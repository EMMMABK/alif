# Generated by Django 4.1.3 on 2023-10-25 14:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news_func', '0003_news_image_alter_news_image_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='image_url',
        ),
    ]