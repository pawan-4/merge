from django.contrib import admin
from django.urls import reverse
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from import_export import resources 
from import_export.admin import ExportActionMixin
from .models import *

#

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'profile_picture', 'dob', 'mobile_number', 'about')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'mobile_number')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    
    def save(self, commit=True):
      
        user = super(UserAdmin, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_date', 'published_date', 'category','display_thumbnail' )
    search_fields = ('title', 'author__username', 'category__slug')
    list_filter = ('created_date', 'published_date', 'category')
    filter_horizontal = ('tags',) 
    
    tags =models.ManyToManyField(Tag,limit_choices_to={"is_active":True})
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
    date_hierarchy = 'created_date'

admin.site.register(Tag,TagAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_date', 'parent_comment')
    search_fields = ('post__title', 'author__username', 'text')
    list_filter = ('created_date', 'post', 'parent_comment')
admin.site.register(Comment,CommentAdmin)


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        list_display = ('username', 'email', 'dob', 'mobile_number')
        fields = ('username', 'email', 'dob', 'mobile_number')


class UsercsvAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = UserResource
    list_filter = ('username', 'dob' ,'email','mobile_number')
    list_display = ('username', 'dob' ,'email','mobile_number')  
    search_fields = ['username']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'

class CustomUserCreationForm(UserCreationForm,):
    class Meta:
        model = User
        fields = '__all__'

class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'is_staff', 'avatar', 'dob', 'mobile_number', 'about'
    )
    search_fields = ('username', 'email', 'first_name', 'last_name', 'mobile_number')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs['form'] = self.add_form
        else:
            kwargs['form'] = self.form
        return super().get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        # Save the user model with the hashed password
        obj.set_password(form.cleaned_data["password"])
        super().save_model(request, obj, form, change)

admin.site.register(User, CustomUserAdmin)
