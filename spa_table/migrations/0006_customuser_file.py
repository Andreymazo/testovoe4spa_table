# Generated by Django 3.2.19 on 2023-05-21 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spa_table', '0005_customuser_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='media/musics/'),
        ),
    ]
