# Generated by Django 4.2.3 on 2023-07-28 20:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=128, null=True)),
                ('phone_number', models.CharField(max_length=13, null=True)),
                ('amount', models.BigIntegerField(null=True)),
                ('person_type', models.CharField(choices=[('physical', 'Jismoniy shaxs'), ('legalentity', 'Yuridik shaxs')], max_length=16, null=True)),
                ('company_name', models.CharField(blank=True, max_length=256, null=True)),
                ('status', models.CharField(choices=[('new', 'Yangi'), ('processing', 'Moderatsiyada'), ('approved', 'Tasdiqlangan'), ('canceled', 'Bekor qilingan')], default='new', max_length=64)),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'University',
                'verbose_name_plural': 'Universities',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200, null=True)),
                ('phone_number', models.CharField(max_length=13, null=True)),
                ('degree', models.CharField(choices=[('bachelor', 'Bakalavr'), ('master', 'Magistr'), ('doctorate', 'Doktorantura')], max_length=64, null=True)),
                ('tution_fee', models.BigIntegerField(null=True)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('university', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='api.university')),
            ],
        ),
        migrations.CreateModel(
            name='Sponsorship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.BigIntegerField(null=True)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('sponsor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sponsorships', to='api.sponsor')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sponsorships', to='api.student')),
            ],
            options={
                'verbose_name': 'Sponsorship',
                'verbose_name_plural': 'Sponsorships',
            },
        ),
    ]
