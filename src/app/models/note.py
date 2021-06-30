from django.db import models

from app.models import WalletUser


class Note(models.Model):
    amount = models.IntegerField()
    # чек
    receipt = models.ImageField(upload_to="receipts\\", null=True, blank=True)
    input_date = models.DateTimeField()
    description = models.CharField(max_length=100)
    over_date = models.DateField(null=True)
    note_type = models.ForeignKey("NoteType", on_delete=models.SET_DEFAULT, default="прочее")
    user = models.ForeignKey(WalletUser, on_delete=models.CASCADE)
    is_closed = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = "note"
        verbose_name = "Запись"
        verbose_name_plural = "Записи"


class NotePaid(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    paid_at = models.DateTimeField()


class NoteType(models.Model):
    name = models.CharField(unique=True, max_length=100)
    income = models.BooleanField(default=True)
    constant = models.BooleanField(default=False)

    class Meta:
        db_table = "note_type"
        verbose_name = "Тип Записи"
        verbose_name_plural = "Типы Записей"
