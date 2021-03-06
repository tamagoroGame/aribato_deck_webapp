# Generated by Django 3.1.7 on 2021-03-05 14:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('name', models.CharField(default=None, max_length=20, verbose_name='名前')),
                ('cost', models.IntegerField(default=None, verbose_name='コスト')),
                ('rarity', models.CharField(choices=[('1', 'B'), ('2', 'A'), ('3', 'S'), ('4', 'SS')], default=None, max_length=5, verbose_name='レア度')),
                ('group', models.CharField(choices=[('zyuken', '287期受験生'), ('ryodan', '幻影旅団'), ('mafian', 'マフィアンコミュニティー'), ('gi', 'G.Iプレイヤー'), ('kimera', 'キメラアント'), ('toubatu', '蟻と闘う者'), ('free', 'フリー')], default=None, max_length=20, verbose_name='GP')),
                ('code', models.IntegerField(default=None, primary_key=True, serialize=False, verbose_name='No.')),
                ('picture', models.ImageField(default=None, upload_to='images/')),
                ('avility', models.TextField(default=None, verbose_name='能力')),
            ],
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('subname', models.CharField(default=None, max_length=20, verbose_name='通り名')),
                ('name', models.CharField(default=None, max_length=20, verbose_name='名前')),
                ('attack', models.IntegerField(default=None, verbose_name='ATK')),
                ('cost', models.IntegerField(default=None, verbose_name='コスト')),
                ('rarity', models.CharField(choices=[('1', 'B'), ('2', 'A'), ('3', 'S'), ('4', 'SS')], default=None, max_length=5, verbose_name='レア度')),
                ('group', models.CharField(choices=[('zyuken', '287期受験生'), ('ryodan', '幻影旅団'), ('mafian', 'マフィアンコミュニティー'), ('gi', 'G.Iプレイヤー'), ('kimera', 'キメラアント'), ('toubatu', '蟻と闘う者'), ('free', 'フリー')], default=None, max_length=20, verbose_name='GP')),
                ('code', models.IntegerField(default=None, primary_key=True, serialize=False, verbose_name='No.')),
                ('picture', models.ImageField(default=None, upload_to='images/')),
                ('avility', models.TextField(default=None, verbose_name='能力')),
                ('combo', models.TextField(default=None, verbose_name='コンボ')),
            ],
        ),
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='DeckOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character_num', models.IntegerField(blank=True, default=None, null=True)),
                ('action_num', models.IntegerField(blank=True, default=None, null=True)),
                ('action', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='deck.action')),
                ('character', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='deck.character')),
                ('deck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deck.deck')),
            ],
        ),
        migrations.AddField(
            model_name='deck',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='deck.Tag'),
        ),
    ]
