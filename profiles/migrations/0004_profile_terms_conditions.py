# Generated by Django 4.2.4 on 2024-01-09 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_alter_contact_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='terms_conditions',
            field=models.BooleanField(default=True),
        ),
    ]
