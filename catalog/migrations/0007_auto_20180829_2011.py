# Generated by Django 2.1 on 2018-08-29 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_auto_20180829_2008'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('all_lean', 'Can view all lean books'),)},
        ),
    ]