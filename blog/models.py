from asyncio import AbstractServer
from django.db import models
from django.utils import timezone
from autoslug import AutoSlugField
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.html import mark_safe
from PIL import Image


class User(AbstractUser):
    
    email = models.EmailField(unique=True, null=True, db_index=True)
    dob = models.DateField(null=True, blank=True)
    mobile_number = models.IntegerField( null=True, blank=True)
    about  = models.CharField(max_length=15, null=True, blank=True)     
    city =models.CharField(max_length=15,)
    country = models.CharField(max_length=15,)
    avatar = models.ImageField(upload_to='profile_pics', null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Corrected line
        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.height > 150 or img.width > 150:
                output_size = (150, 150)
                img.thumbnail(output_size)
                img.save(self.avatar.path)
    def get_email(self):
        return self.email
    
    def __str__(self):
        return self.username

class Category(models.Model):
    title = models.CharField(max_length=200,null=True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    slug = AutoSlugField(populate_from='title',unique=True)
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title    


class Tag(models.Model):
    title = models.CharField(max_length=200,null=True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    slug = AutoSlugField(populate_from='title',unique=True)
    
    def __str__(self):
        return self.title
    

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200,null=True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    slug = AutoSlugField(populate_from='title',unique=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    feature_image=models.ImageField(upload_to='feature_image/',null=True, blank=True)

    def thumbnail_tag(self):
        if self.thumbnail:
            return mark_safe(f'<img src="{self.thumbnail.url}" width="50" height="50" />')
        else:
            return 'No Thumbnail'

    thumbnail_tag.short_description = 'Thumbnail'


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    
    def get_comments(self):
        return self.comments.all()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,)
    reply = models.ForeignKey('self',related_name=("replies"), on_delete = models.CASCADE , blank= True ,null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    name =models.CharField(max_length=200,null=True)


    def __str__(self):
        return "Comment by {self.author} on {self.post.title}"
