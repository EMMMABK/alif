from django.db import models

# Create your models here.

class News(models.Model):
    image = models.URLField()
    title = models.CharField(max_length=255)
    content = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
