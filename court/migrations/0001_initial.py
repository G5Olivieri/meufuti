# Generated by Django 5.0.4 on 2024-04-15 18:18

import django.contrib.postgres.fields
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Court',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField(blank=True, null=True)),
                ('street', models.CharField(max_length=256)),
                ('neighborhood', models.CharField(max_length=128)),
                ('city', models.CharField(max_length=128)),
                ('state', models.CharField(max_length=128)),
                ('zip_code', models.CharField(max_length=32)),
                ('number', models.CharField(max_length=32)),
                ('reference_point', models.CharField(blank=True, max_length=256, null=True)),
                ('facilities', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True, null=True), size=None)),
                ('availability_weeks', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True, null=True), size=7)),
                ('availability_times', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True, null=True), size=24)),
                ('single_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('monthly_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CourtImage',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=256)),
                ('image', models.ImageField(upload_to='upload/')),
                ('court', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='court.court')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('duration', models.DurationField()),
                ('court', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='court.court')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]