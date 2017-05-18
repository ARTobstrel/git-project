# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.template.context_processors import csrf
from django.template.loader import get_template
from django.http import HttpResponse, Http404
from django.shortcuts import render, render_to_response, redirect

from article.forms import CommentForm
from firstapp.settings import BASE_DIR
from article.models import Article, Comments, Keywords, Category


# Create your views here.



def basic_one(request):
    view = 'basic_one'
    html = "<html><body>This is %s view</body></html>" % view
    return HttpResponse(html)

def template_two(request):
    view = 'template_two'
    t = get_template('myview.html')
    html = t.render({'name':view})
    return HttpResponse(html)

def template_three_simple(request):
    view = 'template_three_simple'
    return render_to_response('myview.html', {'name':view})

def articles(request, page_number=1):
    all_articles = Article.objects.all()
    current_page = Paginator(all_articles, 2)
    path = BASE_DIR
    return render_to_response('articles.html', {'articles':current_page.page(page_number),
                                                'path':path,
                                                'username':auth.get_user(request).username,
                                                'keywords':Keywords.objects.all()
                                                }
                              )

def article(request, article_id=1):
    comment_form = CommentForm
    args = {}
    args['keywords'] = Keywords.objects.all()
    args.update(csrf(request))
    args['article'] = Article.objects.get(id=article_id)
    args['comments'] = Comments.objects.filter(comments_article_id=article_id)
    args['form'] = comment_form
    args['username'] = auth.get_user(request).username
    return render_to_response('article.html', args)

def addlike(request, article_id):
    try:
        if article_id in request.COOKIES:
            return_path = request.META.get('HTTP_REFERER', '/') #При добавлении лайка, мы останемся на той же странице что и были
            return redirect(return_path)
        else:
            article = Article.objects.get(id=article_id)
            article.article_likes += 1
            article.save()
            return_path = request.META.get('HTTP_REFERER', '/')
            response = redirect(return_path)
            response.set_cookie(article_id, 'test')
            return response
    except ObjectDoesNotExist:
        raise Http404
    return redirect('/')

def addcomment(request, article_id):
    if request.POST and ('pause' not in request.session):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.comments_author = request.user
            comment.comments_article = Article.objects.get(id=article_id)

            form.save()
            request.session.set_expiry(60)
            request.session['pause'] = True
    return redirect('/articles/get/%s' % article_id)

def keywords(request, id):
    args ={}
    args['keywords'] = Keywords.objects.all()
    args['keyw_s'] = Keywords.objects.get(id=id)
    args['articles'] = Article.objects.filter(keywords__name__exact=args['keyw_s'])
    args['projects'] = Category.objects.all()
    return render(request, 'keypage.html', args)