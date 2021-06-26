from .models import Note
from .models import NotePaid
import datetime


class NoteDto(object):
    def __init__(self, note: Note, need_too_check):
        self.note_model = note
        if need_too_check:
            self.array_of_paid_notes = []
            if not note.note_type.income:
                note_paid = NotePaid.objects.filter(note=note).order_by("-paid_at")
                self.is_this_month_paid = True
                if note_paid:
                    last_time_paid = note_paid[0]
                    now_date = datetime.datetime.now()
                    num_month = (now_date.year - last_time_paid.paid_at.year) * 12 \
                                + (now_date.month - last_time_paid.paid_at.month)
                    if num_month >= 1:
                        self.is_this_month_paid = False
                        self.note_model.input_date = now_date
                        print(self.note_model.input_date)
                    for i in range(0, len(note_paid)):
                        note_ = NoteDto(note, False)
                        note_.note_model.input_date = note_paid[i].paid_at
                        note_.is_this_month_paid = True
                        self.array_of_paid_notes.append(note_)
                    print(self.note_model.input_date)
            else:
                now_date = datetime.datetime.now()
                num_month = (now_date.year - note.input_date.year) * 12 \
                            + (now_date.month - note.input_date.month)
                for i in range(0,num_month + 1):
                    note_dto = NoteDto(note, False)
                    note_dto.note_model.input_date += datetime.timedelta(days=30 * i)
                    self.array_of_paid_notes.append(note_dto)
                    self.is_this_month_paid = False
        print(self.note_model.input_date)
    def __gt__(self, other):
        if self.note_model.input_date > other.note_model.input_date:
            return True
        return False
