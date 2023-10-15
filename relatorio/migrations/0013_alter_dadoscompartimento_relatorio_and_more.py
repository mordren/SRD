# Generated by Django 4.1 on 2023-10-15 18:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('relatorio', '0012_alter_relatoriodescontaminacao_tipo_equipamento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dadoscompartimento',
            name='relatorio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='relatorio.relatoriodescontaminacao'),
        ),
        migrations.RemoveField(
            model_name='relatoriodescontaminacao',
            name='veiculo',
        ),
        migrations.AlterField(
            model_name='veiculo',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='relatorio.cliente'),
        ),
        migrations.AddField(
            model_name='relatoriodescontaminacao',
            name='veiculo',
            field=models.ManyToManyField(to='relatorio.veiculo'),
        ),
    ]
