# Generated by Django 5.1 on 2024-09-09 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_comment_commented_at_alter_like_liked_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
