# Generated by Django 5.0.2 on 2024-03-07 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0004_remove_myuser_emailverificationcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
