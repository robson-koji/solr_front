# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solr_front', '0002_auto_20180619_1146'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RelatedIndexing',
            new_name='RelatedCollectionsCheck',
        ),
    ]
