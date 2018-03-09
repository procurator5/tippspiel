# Generated by Django 2.0.3 on 2018-03-09 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tippspiel', '0007_auto_20180309_1704'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='league',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tippspiel.League'),
        ),
        migrations.AddField(
            model_name='match',
            name='location',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='round',
            field=models.IntegerField(default=1),
        ),
    ]
