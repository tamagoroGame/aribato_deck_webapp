# Generated by Django 3.1.7 on 2021-03-06 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deck', '0002_auto_20210306_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='deck',
            name='like_num',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='いいね数'),
        ),
    ]