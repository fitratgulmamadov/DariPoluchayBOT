# Generated by Django 4.2.3 on 2023-07-22 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_remove_present_tguser_present_from_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='present',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.tguser'),
        ),
    ]