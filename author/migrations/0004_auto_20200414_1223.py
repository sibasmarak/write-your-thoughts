# Generated by Django 2.2.11 on 2020-04-14 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0003_auto_20200414_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='subscribed_author',
            field=models.ManyToManyField(default=None, related_name='subscribers_authors', to='author.Author'),
        ),
    ]
