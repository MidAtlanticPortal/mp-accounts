# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import os


def load_password_dictionary(apps, schema_editor):
    """We're supposed to use data migrations instead of fixtures now. 
    While that makes sense, it measn we have to write stuff like this.  
    """
    PasswordDictionary = apps.get_model('accounts', 'PasswordDictionary')
    db_alias = schema_editor.connection.alias
    
    dictfile = os.path.join(os.path.dirname(__file__), '..', 'fixtures', 
                            '10k_common_passwords.txt')
    if not os.path.exists(dictfile):
        raise Exception("Data file missing")

    with open(dictfile) as data: 
        PasswordDictionary.objects.using(db_alias).bulk_create([
            PasswordDictionary(password=word.strip()) 
            for word in data.readlines()])

def dump_password_dictionary(apps, schema_editor):
    PasswordDictionary = apps.get_model('accounts', 'PasswordDictionary')
    db_alias = schema_editor.connection.alias
    
    PasswordDictionary.objects.using(db_alias).all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_passworddictionary'),
    ]

    operations = [
        migrations.RunPython(load_password_dictionary, dump_password_dictionary)
    ]
