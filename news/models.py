from django.db import models

class NewsCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class News(models.Model):
    title = models.CharField(max_length=200, unique=True)
    content = models.TextField(null=False)
    summary = models.TextField()
    source = models.CharField(max_length=100)
    category = models.ForeignKey(NewsCategory, on_delete=models.PROTECT)
    published_at = models.DateTimeField()
    created_at =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        app_label = 'news'