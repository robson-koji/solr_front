# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pesquisa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='RelatedIndexing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hash_querybuilder', models.IntegerField(help_text=b'Hash do texto da busca do querybuilder, apos o Join com a respectiva collection relacionada.', unique=True, verbose_name='HashQuerybuilder')),
                ('join', models.TextField(max_length=64, verbose_name='Join entre as collections da busca realizada')),
                ('qt_col1', models.IntegerField(help_text=b'', verbose_name='Quantidade do join na coluna 1')),
                ('qt_col2', models.IntegerField(help_text=b'', verbose_name='Quantidade do join na coluna 2')),
                ('created_date', models.CharField(max_length=64, verbose_name='Data de cria\xe7\xe3o da busca')),
                ('modified_date', models.CharField(max_length=64, verbose_name='\xdaltima atualiza\xe7\xe3o da busca')),
            ],
        ),
    ]
