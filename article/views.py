from django.shortcuts import render,redirect,reverse
from django.shortcuts import HttpResponse
from .models import ArticlePost
from django.contrib.auth.models import User
from .forms import ArticlePostForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.
def article_list(request):
    if request.GET.get('order')=='total_views':
        articles_list=ArticlePost.objects.all().order_by('-total_views')
        order = 'total_views'
    else:
        articles_list = ArticlePost.objects.all()
        order = 'normal'

    pagenator=Paginator(articles_list,6)
    page=request.GET.get('page')
    articles=pagenator.get_page(page)

    context = {'articles': articles,'order':order}
    return render(request, 'article/list.html', context)


import markdown


def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)

    article.total_views+=1
    article.save(update_fields=['total_views',])

    # 將markdown渲染成html
    article.body = markdown.markdown(article.body,
     extensions=[
         # 包含 缩写、表格等常用扩展
         'markdown.extensions.extra',
         # 语法高亮扩展
         'markdown.extensions.codehilite',
     ])

    context = {'article': article}

    return render(request, 'article/detail.html', context)

@login_required(login_url='/userprofile/login/')
def article_create(request):
    article_post_form = ArticlePostForm(data=request.POST or None)
    if request.method=="POST":
        if article_post_form.is_valid():
            # 保存 但不提交
            new_article = article_post_form.save(commit=False)
            # 指定id=1的User為作者
            new_article.author=User.objects.get(id=request.user.id)

            new_article.save()

            return redirect('article:article_list')
        else:
            return HttpResponse("內容有誤 請重新填寫")

    return render(request,'article/create.html',locals())

def article_delete(request, id):
    # 根据 id 获取需要删除的文章
    article = ArticlePost.objects.get(id=id)
    # 调用.delete()方法删除文章
    article.delete()
    # 完成删除后返回文章列表
    return redirect("article:article_list")

@login_required(login_url='/userprofile/login/')
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求")

@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    """
    更新文章的视图函数
    通过POST方法提交表单，更新titile、body字段
    GET方法进入初始表单页面
    id： 文章的 id
    """

    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=id)

    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")

    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的 title、body 数据并保存
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("article:article-detail", id=id)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = { 'article': article, 'article_post_form': article_post_form }
        # 将响应返回到模板中
        return render(request, 'article/update.html', context)


