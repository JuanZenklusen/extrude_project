# Generated by Django 4.2.4 on 2023-11-21 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0026_matricula_exam_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessons',
            name='visible',
            field=models.BooleanField(default=False),
        ),
    ]
