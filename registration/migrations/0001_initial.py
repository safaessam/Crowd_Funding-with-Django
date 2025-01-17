# Generated by Django 5.0.2 on 2024-03-09 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=30)),
                ('mobile_phone', models.CharField(max_length=11)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='static/profile_pictures/')),
                ('is_active', models.BooleanField(default=False)),
                ('isEmailVerified', models.BooleanField(default=False)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('facebook_profile', models.URLField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserEmailVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('code', models.CharField(default=0, max_length=6)),
                ('expireTime', models.DateTimeField()),
            ],
        ),
    ]
