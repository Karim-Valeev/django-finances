import datetime

from .dto import NoteDto
from .models import WalletUser, NoteType, Note, NotePaid
import operator


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
    notes_final.sort(key=operator.attrgetter('input_date'),reverse=True)
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


def pay_note(user, pk):
    note = Note.objects.filter(id=pk).select_related("user")[0]
    if note.user == user:
        paid = NotePaid(note=note, paid_at=datetime.datetime.now())
        paid.save()


def delete_note(user, pk):
    note = Note.objects.filter(id=pk).select_related("user")[0]
    if note.user == user:
        note.delete()

def make_all_chart(user):
    pass
