# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visualize', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='codedata',
            name='code_key',
            field=models.TextField(default='test'),
            preserve_default=False,
        ),
    ]
