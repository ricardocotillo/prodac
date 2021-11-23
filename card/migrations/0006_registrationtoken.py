# Generated by Django 3.2.8 on 2021-11-23 00:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0005_card_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=500, null=True)),
                ('card', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tokens', to='card.card')),
            ],
        ),
    ]
