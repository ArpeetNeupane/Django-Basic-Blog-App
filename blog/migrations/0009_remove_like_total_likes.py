# Generated by Django 5.1 on 2024-09-10 04:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_rename_count_like_total_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='total_likes',
        ),
    ]
