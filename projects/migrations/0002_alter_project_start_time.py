# Generated by Django 5.0.2 on 2024-03-04 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='start_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]