from django.contrib import admin
from .models import NoteType, Note, NotePaid
from .models import WalletUser


admin.site.register(WalletUser)
admin.site.register(Note)
admin.site.register(NoteType)
admin.site.register(NotePaid)
