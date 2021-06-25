from django.db import models

from app.models import WalletUser


class Note(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField()
    receipt = models.ImageField()
    input_date = models.DateTimeField()
    constant = models.BooleanField()
    description = models.CharField(max_length=100)
    over_date = models.DateField()
    note_type = models.ForeignKey("NoteType", on_delete=models.SET_DEFAULT, default="прочее")
    user = models.ForeignKey(WalletUser, on_delete=models.CASCADE)

    class Meta:
        db_table = "note"
        verbose_name = "Запись"
        verbose_name_plural = "Записи"


class NoteType(models.Model):
    name = models.CharField(unique=True, max_length=100)
    income = models.BooleanField()

    class Meta:
        db_table = "note_type"
        verbose_name = "Тип Записи"
        verbose_name_plural = "Типы Записей"
