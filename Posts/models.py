from __future__ import unicode_literals
from Accounts.models import User
from django.db import models
from django.utils import timezone

import datetime

# Create your models here.


# model manager
class Postmanager(models.Manager):
    def active(self, *args, **kwargs):
        return super(Postmanager, self).filter(draft=False, publish=timezone.now())


# Creating a Category Model
class Category(models.Model):
    category_name = models.CharField(max_length=30)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name

# Model Posts


class MyPosts(models.Model):
    class Meta:
        verbose_name_plural = "Posts"

    # fields
    post_title = models.CharField(max_length=100)
    post_content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(
        auto_now=False, auto_now_add=False)
    image = models.ImageField(
        null=True, blank=True, width_field="width_field", height_field="height_field",
    )
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    # Add User Foreing key
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="user_post", null=True, blank=True)

    # adding a category forieng key
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='post_category', null=True)

    # link model manager our model
    objects = Postmanager()
    # return self.title whene queryseting

    def __str__(self):
        # For python 3
        return self.post_title

    def __unicode__(self):
        return self.post_title  # for python 2

        # define a new default image
    @property
    def default_pic(self):
        default_img = 'Use_Default/d2.jpg'
        if self.image:
            return self.image
        else:
            return default_img

        # Resieze uploaded Posts images
    def save(self, *args, **kwargs):

        # these imports will only work inside of this function
        from PIL import Image
        from io import BytesIO
        from django.core.files.base import ContentFile

        # Start writing the method ..
        img = Image.open(self.image)
        resized_img = img.resize((5825, 2802), Image.ANTIALIAS)
        new_image = BytesIO()

        if img.format == 'JPEG':
            resized_img.save(new_image, format='JPEG')

        elif img.format == 'PNG':
            resized_img.sve(new_image, format='PNG')

        temp_name = self.image.name
        self.image.delete(save=False)

        self.image.save(
            temp_name,
            content=ContentFile(new_image.getvalue()),
            save=False
        )

        # call the super
        super(MyPosts, self).save(*args, **kwargs)


# Creating a Comment model
class Comments(models.Model):
    post_name = models.ForeignKey(
        MyPosts, related_name='post_comment', on_delete=models.CASCADE, blank=True)
    user = models.ForeignKey(
        User, related_name='user_comment', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Comment Something !!!')
    created_at = models.DateTimeField(default=timezone.now)
    approved_comments = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = ' Users Comments'

# str method
    def __str__(self):
        return self.text
