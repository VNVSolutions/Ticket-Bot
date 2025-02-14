# Generated by Django 3.1.1 on 2024-09-24 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConditionsText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True)),
                ('link', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'conditions_text',
            },
        ),
        migrations.AlterField(
            model_name='conditions',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
