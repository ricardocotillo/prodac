# Generated by Django 3.2.8 on 2021-10-14 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0014_landing'),
    ]

    operations = [
        migrations.AddField(
            model_name='landing',
            name='message',
            field=models.CharField(default='', max_length=150),
            preserve_default=False,
        ),
    ]
