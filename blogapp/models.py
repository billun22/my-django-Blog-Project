from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Article(models.Model):
    
    title = models.CharField(max_length=255, default="Untitled")
    content = models.TextField()
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="articles")
    publish_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='article/image/', null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField()
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user.username} - {self.body[:20]}"

    def is_reply(self):
        return self.parent is not None