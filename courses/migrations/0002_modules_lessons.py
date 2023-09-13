# Generated by Django 4.2.4 on 2023-09-05 20:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Modules',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('subtitle', models.CharField(blank=True, max_length=50, null=True)),
                ('nro_order', models.IntegerField()),
                ('slug', models.SlugField(unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.courses')),
            ],
        ),
        migrations.CreateModel(
            name='Lessons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('subtitle', models.CharField(blank=True, max_length=500, null=True)),
                ('nro_order', models.IntegerField()),
                ('video', models.CharField(blank=True, max_length=400, null=True)),
                ('text1', models.TextField(blank=True, default='', null=True)),
                ('text2', models.TextField(blank=True, default='', null=True)),
                ('text3', models.TextField(blank=True, default='', null=True)),
                ('slug', models.SlugField(unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.modules')),
            ],
        ),
    ]