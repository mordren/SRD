# Generated by Django 4.1 on 2023-10-10 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relatorio', '0008_dadoscompartimento_volumear_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dadoscompartimento',
            name='tempo',
            field=models.IntegerField(),
        ),
    ]
