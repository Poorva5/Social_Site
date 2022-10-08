from email.policy import default
from django.db import models
from account.models import UserData
from django.urls import reverse
from django.utils.text import slugify
from helper.models import BaseModel


class PostData(models.Model):
    caption = models.TextField()
    slug = models.CharField(max_length=300)
    image = models.ImageField(upload_to='posts/%Y/%m/%d', null=True, blank=True)
    author = models.ForeignKey(UserData, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    uploaded_at = models.DateTimeField(auto_now=True)
    user_like = models.ManyToManyField(UserData, related_name='posts_liked', blank=True, default=None)

    def __str__(self):
        return self.caption

    def get_absolute_url(self):
        return reverse("post_detail", args=[self.created_at.year, self.created_at.month, self.created_at.day, self.slug])

    def save(self, *args, **kwargs):
        self.slug = '-'.join((slugify(self.caption), slugify(self.author)))
        super(PostData, self).save(*args, **kwargs)
    
    def number_of_likes(self):
        return self.user_like.count()

    class Meta:
        ordering = ['-uploaded_at',]