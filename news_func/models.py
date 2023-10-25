from django.db import models

# Create your models here.

class News(models.Model):
    image = models.ImageField(upload_to='news_images/')
    title = models.CharField(max_length=255)
    content = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return ''