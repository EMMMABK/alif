# Generated by Django 4.1.3 on 2023-10-17 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization_func', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='repeat_password',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]
