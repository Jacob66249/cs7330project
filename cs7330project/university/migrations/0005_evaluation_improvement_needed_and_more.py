# Generated by Django 5.0.4 on 2024-04-28 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0004_alter_section_unique_together_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluation',
            name='improvement_needed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
    ]