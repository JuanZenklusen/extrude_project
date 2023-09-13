# Generated by Django 4.2.4 on 2023-09-05 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('description', models.CharField(max_length=300)),
                ('price', models.IntegerField(default=1000)),
                ('payment_installments', models.IntegerField(blank=True, default=1, null=True)),
                ('price_payment_installments', models.IntegerField(blank=True, default=1000, null=True)),
                ('link_mp', models.CharField(blank=True, max_length=100, null=True)),
                ('program', models.CharField(blank=True, max_length=300, null=True)),
                ('img', models.ImageField(default='course-default.jpg', upload_to='course_images')),
                ('modality', models.CharField(blank=True, max_length=50, null=True)),
                ('requirements', models.TextField(blank=True, max_length=1500, null=True)),
                ('lesson_duration', models.CharField(blank=True, max_length=20, null=True)),
                ('weekly_frequency', models.CharField(blank=True, max_length=1, null=True)),
                ('duration_in_weeks', models.CharField(blank=True, max_length=50, null=True)),
                ('course_program', models.CharField(blank=True, max_length=300, null=True)),
                ('text_include', models.TextField(blank=True, max_length=1500, null=True)),
                ('slug', models.SlugField(unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]