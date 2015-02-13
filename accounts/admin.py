from django.contrib import admin

from models import PasswordDictionary
admin.site.register(PasswordDictionary)

from models import UserData
admin.site.register(UserData)

from models import EmailVerification
admin.site.register(EmailVerification)

