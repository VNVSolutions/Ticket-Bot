# Generated by Django 3.1.1 on 2024-09-24 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conditions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'conditions',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.BigIntegerField(null=True)),
                ('username', models.CharField(max_length=256, null=True)),
                ('name', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'userprofile',
            },
        ),
    ]
