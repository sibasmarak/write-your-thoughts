# Generated by Django 2.2.11 on 2020-04-14 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='normaluser',
            name='subscribed_author',
            field=models.ManyToManyField(null=True, related_name='subscribers_users', to='author.Author'),
        ),
    ]