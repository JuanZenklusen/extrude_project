# Generated by Django 4.2.4 on 2023-11-13 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0017_courses_visible'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessons',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to='pdfs'),
        ),
    ]