# Generated by Django 3.2.19 on 2023-05-21 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spa_table', '0006_customuser_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='file',
            new_name='file_mp3',
        ),
        migrations.AddField(
            model_name='customuser',
            name='file_wav',
            field=models.FileField(blank=True, null=True, upload_to='media/musics/'),
        ),
    ]
