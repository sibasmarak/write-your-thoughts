# Generated by Django 2.2.11 on 2020-04-14 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200414_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='normaluser',
            name='subscribed_author',
            field=models.ManyToManyField(blank=True, null=True, related_name='subscribers_users', to='author.Author'),
        ),
    ]