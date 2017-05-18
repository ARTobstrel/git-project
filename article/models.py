# -*- coding: utf-8 -*-
#__unicode__ on Python 2
from __future__ import unicode_literals

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from mptt.models import MPTTModel, TreeForeignKey
import mptt

class Keywords(models.Model):
    class Meta():
        db_table = 'keywords'

    name = models.CharField(max_length=50, unique=True, verbose_name='теги')

    def __unicode__(self):
        return self.name

class Category(MPTTModel):
    class Meta():
        db_table = 'category'
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'
        ordering = ('tree_id', 'level')

    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, verbose_name='Родительский класс')

    def __unicode__(self):  #__unicode__ on Python 2
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

mptt.register(Category, order_insertion_by=['name'])

class Article(models.Model):
    class Meta():
        db_table = 'article'

    article_title = models.CharField(max_length=200)
    article_text = RichTextUploadingField()
    article_date = models.DateTimeField()
    article_likes = models.IntegerField(default=0)
    article_image = models.ImageField(null=True, blank=True, upload_to='images/', verbose_name='Изображение')
    category = TreeForeignKey(Category, blank=True, null=True, related_name='cat')
    keywords = models.ManyToManyField(Keywords, related_name='keywords', related_query_name='keyword', verbose_name='теги')

    def __unicode__(self):  #__unicode__ on Python 2
        return self.article_title

    def bit(self):
        if self.article_image:
            return u'<img src="%s" width="/0"/>' % self.article_image.url
        else:
            return u'(none)'
    bit.short_descriptio = u'Изображение'
    bit.allow_tags = True

class Comments(models.Model):
    class Meta():
        db_table = 'comments'

    comments_text = models.TextField(verbose_name='Текст комментария')
    comments_article = models.ForeignKey(Article)
    comments_date = models.DateTimeField(u'date', auto_now=True)
    comments_author = models.ForeignKey(User)

class Tesla(models.Model):

    tesla_text = models.TextField(verbose_name='Tesla')