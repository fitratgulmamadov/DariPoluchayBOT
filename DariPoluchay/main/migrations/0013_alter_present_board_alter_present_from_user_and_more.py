# Generated by Django 4.2.3 on 2023-07-23 00:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_present_board_alter_present_from_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='present',
            name='board',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main.board'),
        ),
        migrations.AlterField(
            model_name='present',
            name='from_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='from_usr', to='main.tguser'),
        ),
        migrations.AlterField(
            model_name='present',
            name='to_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main.tguser'),
        ),
    ]
