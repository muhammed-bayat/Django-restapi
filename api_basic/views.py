from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
# Create your views here.




 
@csrf_exempt
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializers = ArticleSerializer(articles, many=True)
        return JsonResponse(serializers.data, safe=False)
        print("articles::",articles)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializers = ArticleSerializer(data=data)
        if serializers.is_valid():
            serializers.save()
            return JsonResponse(serializers.data, status=201)
            print("serializers::",serializers)

        return JsonResponse(serializers.errors, status=400)
    
    
@csrf_exempt
def article_detail(request, pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializers = ArticleSerializer(article)
        return JsonResponse(serializers.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializers = ArticleSerializer(article, data=data)
        if serializers.is_valid():
            serializers.save()
            return JsonResponse(serializers.data)
        return JsonResponse(serializers.errors, status=400)

    elif request.method == 'DELETE':
        article.delete()
        return HttpResponse(status=204)