# Generated by Django 4.2.4 on 2023-11-13 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0021_remove_lessons_link_pdf_lessons_pdf'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lessons',
            name='document',
        ),
    ]
