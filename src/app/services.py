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
