from ..models import *
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
import markdown

def index(request, pk):
    post = get_object_or_404(Fmark, pk=pk)
    # 记得在顶部引入 markdown 模块
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                  ])
    print(post.body)
    return render(request, 'fmark/fmark_index.html', locals())