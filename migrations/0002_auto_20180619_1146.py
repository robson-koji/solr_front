# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solr_front', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='relatedindexing',
            name='modified_date',
        ),
        migrations.AddField(
            model_name='relatedindexing',
            name='counted_date',
            field=models.DateTimeField(null=True, verbose_name='\xdaltima contagem da busca relacionada'),
        ),
        migrations.AddField(
            model_name='relatedindexing',
            name='indexed_date',
            field=models.DateTimeField(null=True, verbose_name='\xdaltima indexa\xe7\xe3o da sub-collection'),
        ),
        migrations.AlterField(
            model_name='relatedindexing',
            name='created_date',
            field=models.DateTimeField(verbose_name='Data de cria\xe7\xe3o da busca'),
        ),
    ]
