# Generated by Django 4.2.4 on 2023-11-13 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0018_lessons_pdf'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lessons',
            name='pdf',
        ),
        migrations.AddField(
            model_name='lessons',
            name='link_pdf',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
