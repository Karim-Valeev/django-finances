from .models import Note
from .models import NotePaid
import datetime


class NoteDto(object):
    def __init__(self, note: Note, need_too_check):
        self.note_type = note.note_type
        self.id = note.id
        self.description = note.description
        self.amount = note.amount
        self.input_date = note.input_date
        if need_too_check:
            self.array_of_paid_notes = []
            if not note.note_type.income:
                note_paid = NotePaid.objects.filter(note=note).order_by("-paid_at")
                self.is_this_month_paid = True
                if note_paid:
                    begin_with = 1
                    last_time_paid = note_paid[0]
                    now_date = datetime.datetime.now()
                    num_month = (now_date.year - last_time_paid.paid_at.year) * 12 \
                                + (now_date.month - last_time_paid.paid_at.month)
                    if num_month >= 1:
                        self.is_this_month_paid = False
                        self.input_date = now_date
                        begin_with = 0
                    for i in range(begin_with, len(note_paid)):
                        note_ = NoteDto(note, False)
                        note_.input_date = note_paid[i].paid_at
                        note_.is_this_month_paid = True
                        self.array_of_paid_notes.append(note_)
                else:
                    self.is_this_month_paid = False
            else:
                now_date = datetime.datetime.now()
                num_month = (now_date.year - note.input_date.year) * 12 \
                            + (now_date.month - note.input_date.month)
                for i in range(0, num_month + 1):
                    note_dto = NoteDto(note, False)
                    note_dto.input_date += datetime.timedelta(days=30 * i)
                    self.array_of_paid_notes.append(note_dto)
                    self.is_this_month_paid = False
        print(self.input_date)

    def __gt__(self, other):
        if self.input_date > other.input_date:
            return True
        return False
