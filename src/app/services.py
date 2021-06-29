import io

from google.cloud import vision
import pandas as pd
from .models import WalletUser, NoteType, Note


def register_user(email, name, password):
    user = WalletUser(email=email, name=name)
    user.set_password(password)
    user.save()
    return user


def get_main_page_data(user):
    note_types_income = NoteType.objects.filter(income=True)
    note_types_consumption = NoteType.objects.filter(income=False)
    notes = Note.objects.filter(user=user)
    return {"note_types_income": note_types_income, "note_types_consumption": note_types_consumption, "notes": notes}


def new_note(form, user):
    note = Note(amount=form.cleaned_data['amount'], input_date=form.cleaned_data['date'],
                description=form.cleaned_data['description'], user=user)
    note_type = NoteType.objects.get(name=form.cleaned_data['note_type'])
    note.note_type = note_type
    note.save()


def get_text_from_image(file_name):
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

    return (df['description'][0])
