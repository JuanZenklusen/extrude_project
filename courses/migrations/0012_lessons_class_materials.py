# Generated by Django 4.2.4 on 2023-10-24 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_matricula_lessons_viewed_alter_matricula_last_lesson'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessons',
            name='class_materials',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]