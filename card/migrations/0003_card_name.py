# Generated by Django 3.2.8 on 2021-11-10 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0002_card_facebook'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='name',
            field=models.CharField(default='FerreProdac', max_length=250),
        ),
    ]
