# Generated by Django 4.2.4 on 2023-09-28 22:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_alter_modulerating_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='matricula',
            name='last_lesson',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.lessons'),
        ),
    ]
