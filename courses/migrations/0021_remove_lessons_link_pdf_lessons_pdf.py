# Generated by Django 4.2.4 on 2023-11-13 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0020_alter_lessons_link_pdf'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lessons',
            name='link_pdf',
        ),
        migrations.AddField(
            model_name='lessons',
            name='pdf',
            field=models.FileField(blank=True, null=True, unique=True, upload_to='pdfs'),
        ),
    ]
