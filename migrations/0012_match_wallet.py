# Generated by Django 2.0.3 on 2018-03-17 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_bitcoin', '0001_initial'),
        ('tippspiel', '0011_bettype_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='wallet',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='django_bitcoin.Wallet'),
            preserve_default=False,
        ),
    ]
