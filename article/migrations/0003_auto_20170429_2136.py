# -*- coding: utf-8 -*-
# Generated by Django 1.11rc1 on 2017-04-29 21:36
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_article_article_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_text',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]