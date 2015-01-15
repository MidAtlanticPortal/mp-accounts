# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='profile_image',
            field=models.URLField(default=b'/static/accounts/marco_user.png', help_text=b"URL to the user's profile image."),
            preserve_default=True,
        ),
    ]
