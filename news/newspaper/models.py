from django.db import models
# # добавил 20.12
from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
import pytz
from django.utils import timezone


#
# class Category(models.Model):
#     name = models.CharField(max_length=255)
#
#     def __str__(self):
#         return self.name
#
#     def get_absolute_url(self):
#         return reverse('home')
#
# class MyModel(models.Model):
#     name = models.CharField(max_length=100)
#     kind = models.ForeignKey(
#         Category,
#         on_delete=models.CASCADE,
#         related_name='kinds',
#         verbose_name=pgettext_lazy('help text for MyModel model', 'This is the help text'),
#     )


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.session.get('django_timezone')
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)

class Appointment(models.Model):
    date = models.DateField(
        default=datetime.utcnow,
    )
    client_name = models.CharField(
        max_length=200
    )
    message = models.TextField()

    def __str__(self):
        return f'{self.client_name}: {self.message}'
#
#
#
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home')

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    kind = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='kinds',
        verbose_name=pgettext_lazy('help text for MyModel model', 'This is the help text'),
    )

#
#
class Author(models.Model):

   user = models.OneToOneField(User, on_delete=models.CASCADE)
   #user_rate = models.IntegerField(default=0)
   full_name = models.CharField(max_length=255)
#
#
class Post(models.Model):

    title = models.CharField(max_length = 255)
    title_tag = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    body = models.TextField()
    post_date = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='blog_posts')
    category = models.CharField(max_length = 255, default='news')
    dislikes = models.ManyToManyField(Author, related_name='blog_posts')

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()


    def __str__(self):
        return self.title + ' | ' + str(self.author)


    def get_absolute_url(self):
        return reverse('home')
#

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)
#
# # Create your models here.
