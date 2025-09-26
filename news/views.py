from django.utils import timezone
from datetime import timedelta
from .models import News
from news.serializers import NewsSerializer, NewsCategorySerializer
from news.models import NewsCategory
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework.response import Response

class NewsPageNumberPagination(PageNumberPagination):
    page_size = 10 
    page_size_query_param = 'page_size' 
    max_page_size = 100 


class NewsViewSet(viewsets.ModelViewSet):

    queryset = News.objects.all().order_by('-published_at')
    serializer_class = NewsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        categories_param = self.request.query_params.get('categories', None)
        
        if categories_param is not None:
            category_list = [c.strip() for c in categories_param.split(',') if c.strip()]
            
            if category_list:
                queryset = queryset.filter(category__name__in=category_list)

        period = self.request.query_params.get('period', None)
        now = timezone.now()
        
        if period == 'day':
            start = now - timedelta(days=1)
            queryset = queryset.filter(published_at__gte=start)
        elif period == 'week':
            start = now - timedelta(days=now.weekday())
            start = start.replace(hour=0, minute=0, second=0, microsecond=0)
            queryset = queryset.filter(published_at__gte=start)
        elif period == 'month':
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            queryset = queryset.filter(published_at__gte=start)

        return queryset
    
class NewsCategoryViewSet(viewsets.ModelViewSet):
    queryset = NewsCategory.objects.all()
    serializer_class = NewsCategorySerializer
    pagination_class = None  

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        
        except Exception as e:
            return Response({'detail': 'Erro ao recuperar categorias.'}, status=500)
