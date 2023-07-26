# Generated by Django 4.2.3 on 2023-07-18 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Board name')),
                ('present_price', models.IntegerField(verbose_name='Present price')),
            ],
        ),
        migrations.CreateModel(
            name='TgUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('ch_id', models.IntegerField(verbose_name='ChatId')),
                ('join_date', models.DateTimeField(auto_now=True, verbose_name='Join time')),
                ('link', models.CharField(max_length=150, verbose_name='Link')),
                ('status', models.CharField(choices=[('R', 'Red'), ('G', 'Green'), ('W', 'White')], default='W', max_length=1, verbose_name='Status')),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.board')),
                ('father', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.tguser')),
            ],
        ),
        migrations.CreateModel(
            name='RefLinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=500)),
                ('tguser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.tguser')),
            ],
        ),
        migrations.CreateModel(
            name='Present',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.board')),
                ('tguser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.tguser')),
            ],
        ),
    ]
