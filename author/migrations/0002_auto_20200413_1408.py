# Generated by Django 2.2.11 on 2020-04-13 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['-rating']},
        ),
    ]
