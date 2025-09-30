from news.models import News, NewsCategory
from rest_framework import serializers

class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ['id', 'name']

class NewsSerializer(serializers.ModelSerializer):
    category = NewsCategorySerializer(read_only=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'summary', 'source', 'category', 'published_at', 'created_at']
        
class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ['id', 'name']