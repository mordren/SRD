# Generated by Django 4.1 on 2023-10-17 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('relatorio', '0014_remove_relatoriodescontaminacao_veiculo_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Finalidade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finalidade', models.CharField(choices=[('1', 'Inspeção'), ('2', 'Manunteção'), ('3', 'Reparo'), ('4', 'Reforma'), ('5', 'Verificao metrológica')], default='1', help_text='Finalidade Descontaminação', max_length=50, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='dadoscompartimento',
            name='ultimo_produto_transportado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='relatorio.produtotransportado', verbose_name='Produto Perigoso Transportado'),
        ),
        migrations.RemoveField(
            model_name='relatoriodescontaminacao',
            name='finalidade_descontaminacao',
        ),
        migrations.AddField(
            model_name='relatoriodescontaminacao',
            name='finalidade_descontaminacao',
            field=models.ManyToManyField(to='relatorio.finalidade'),
        ),
    ]
