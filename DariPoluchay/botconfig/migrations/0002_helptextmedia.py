# Generated by Django 4.2.3 on 2023-07-20 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('botconfig', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HelpTextMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('text', models.TextField()),
                ('img', models.ImageField(upload_to='users/%Y/%m/%d/')),
            ],
        ),
    ]
