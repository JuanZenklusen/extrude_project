# Generated by Django 4.2.4 on 2023-12-18 22:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0028_homework_submithomework'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submithomework',
            name='submitted_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.CreateModel(
            name='QuestionsAndAnswers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('q1', models.IntegerField(default=None, null=True)),
                ('q2', models.IntegerField(default=None, null=True)),
                ('q3', models.IntegerField(default=None, null=True)),
                ('q4', models.IntegerField(default=None, null=True)),
                ('q5', models.IntegerField(default=None, null=True)),
                ('q6', models.IntegerField(default=None, null=True)),
                ('q7', models.IntegerField(default=None, null=True)),
                ('q8', models.IntegerField(default=None, null=True)),
                ('q9', models.IntegerField(default=None, null=True)),
                ('q10', models.IntegerField(default=None, null=True)),
                ('a1', models.IntegerField(default=None, null=True)),
                ('a2', models.IntegerField(default=None, null=True)),
                ('a3', models.IntegerField(default=None, null=True)),
                ('a4', models.IntegerField(default=None, null=True)),
                ('a5', models.IntegerField(default=None, null=True)),
                ('a6', models.IntegerField(default=None, null=True)),
                ('a7', models.IntegerField(default=None, null=True)),
                ('a8', models.IntegerField(default=None, null=True)),
                ('a9', models.IntegerField(default=None, null=True)),
                ('a10', models.IntegerField(default=None, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.exam')),
                ('matricula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.matricula')),
            ],
        ),
    ]
