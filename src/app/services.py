import io

from google.cloud import vision
import pandas as pd
import datetime

from .dto import NoteDto
from .models import WalletUser, NoteType, Note, NotePaid
import operator
import plotly.express as px
from plotly.offline import download_plotlyjs, plot


def register_user(email, name, password):
    user = WalletUser(email=email, name=name)
    user.set_password(password)
    user.save()
    return user


def get_main_page_data(user):
    note_types_income = NoteType.objects.filter(income=True)
    note_types_consumption = NoteType.objects.filter(income=False)
    notes_db = Note.objects.filter(user=user).select_related("note_type")
    notes_final = []
    for note in notes_db:
        notes_final += refresh_note(note)
    notes_final.sort(key=operator.attrgetter('input_date'), reverse=True)
    return {"note_types_income": note_types_income, "note_types_consumption": note_types_consumption,
            "notes": notes_final}


def refresh_note(note: Note):
    result = []
    if note.note_type.constant:
        dto = NoteDto(note, True)
        result.append(dto)
        result += dto.array_of_paid_notes
    else:
        dto = NoteDto(note, False)
        result.append(dto)
    return result


def new_note(form, user):
    note = Note(amount=form.cleaned_data['amount'], input_date=form.cleaned_data['date'],
                description=form.cleaned_data['description'], user=user)
    note_type = NoteType.objects.get(name=form.cleaned_data['note_type'])
    note.note_type = note_type
    note.save()


def process_receipt(file, user):
    note_type = NoteType.objects.filter(name="Прочее-")
    note = Note(input_date=datetime.datetime.now(),
                receipt=file, note_type=note_type[0], description="Чек", amount=0)
    note.user = user
    note.save()

    get_text_from_image(note.receipt.path, note)


def get_text_from_image(file_name, note):
    client = vision.ImageAnnotatorClient()

    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    # construct an image instance
    image = vision.Image(content=content)

    # annotate Image Response
    response = client.text_detection(image=image, image_context={"language_hints": ["ru"]}, )  # returns TextAnnotation
    df = pd.DataFrame(columns=['locale', 'description'])

    texts = response.text_annotations
    for text in texts:
        df = df.append(
            dict(
                locale=text.locale,
                description=text.description
            ),
            ignore_index=True
        )

    print(df['description'][0])
    #note.amount = df['description'][0]
    #note.save()
    # return (df['description'][0])


def pay_note(user, pk):
    note = Note.objects.filter(id=pk).select_related("user")[0]
    if note.user == user:
        paid = NotePaid(note=note, paid_at=datetime.datetime.now())
        paid.save()


def delete_note(user, pk):
    note = Note.objects.filter(id=pk).select_related("user")[0]
    if note.user == user:
        note.delete()


def make_chart(user_notes, name):
    frame = pd.DataFrame.from_records(
        user_notes.values(
            "note_type__name",
            "amount",
        )
    ).rename(
        columns={
            "note_type__name": "note_type"
        }
    )
    fig = px.pie(frame, values='amount', names="note_type", title=name,
                 color_discrete_sequence=px.colors.sequential.RdBu)
    div = plot(fig, auto_open=False, output_type="div")
    return div


def make_all_chart(user):
    user_notes = Note.objects.filter(user=user).select_related("note_type")

    if user_notes:
        return make_chart(user_notes, "За все время.")
    else:
        return "Ничего нет."


def make_monthly_chart(user):
    user_notes = Note.objects.filter(user=user).select_related("note_type")
    user_note_month = []
    for note in user_notes:
        if not note.note_type.constant:
            now_date = datetime.datetime.now()
            num_month = (now_date.year - note.input_date.year) * 12 \
                        + (now_date.month - note.input_date.month)
            if num_month >= 1:
                user_note_month.append(note)
        else:
            user_note_month.append(note.id)

    user_notes = Note.objects.filter(id__in=user_note_month).select_related("note_type")

    if user_notes:
        return make_chart(user_notes, "За месяц")
    else:
        return "Ничего нет"
