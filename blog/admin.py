from django.contrib import admin
from .models import *
from django.urls import reverse
from import_export import resources 
from import_export.admin import ExportActionMixin
#admin.site.register(Post)
#admin.site.register(Category)
#admin.site.register(Tag)
#admin.site.register(User)
#py admin.site.register(Comment)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'profile_picture', 'dob', 'mobile_number', 'about')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'mobile_number')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_date', 'published_date', 'category','display_thumbnail' )
    search_fields = ('title', 'author__username', 'category__slug')
    list_filter = ('created_date', 'published_date', 'category')
    def display_thumbnail(self, obj):
        return obj.thumbnail_tag()

    display_thumbnail.short_description = 'Thumbnail'

    
    
    def view_on_site(self, obj=None):
        url = reverse("post_detail", kwargs={'slug': obj.slug})
        return url
    
admin.site.register(Post,PostAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date', 'published_date')
    search_fields = ('title',)
    list_filter = ('created_date', 'published_date')
admin.site.register(Category,CategoryAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date', 'published_date')
    search_fields = ('title',)
    list_filter = ('created_date', 'published_date')

admin.site.register(Tag,TagAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_date', 'parent_comment')
    search_fields = ('post__title', 'author__username', 'text')
    list_filter = ('created_date', 'post', 'parent_comment')
admin.site.register(Comment,CommentAdmin)


class UserResource(resources.ModelResource):

    class Meta:
        model=User
        list_display=('username','email','dob','mobile_number')
        fields=('username','email','dob','mobile_number')


class UsercsvAdmin(ExportActionMixin,admin.ModelAdmin):
    resource_class = UserResource

admin.site.register(User,UsercsvAdmin)