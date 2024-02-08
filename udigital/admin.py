from django.contrib import admin
from django_reverse_admin import ReverseModelAdmin
from udigital.forms import UserAdminForm
from udigital.models import User, Post, Comment


class UserAdmin(ReverseModelAdmin):
    inline_type = 'stacked'
    inline_reverse = ['phone_number']
    list_display = (
        'date_joined', 'first_name', 'last_name', 'email', 'phone_number', 'last_login', 'is_active', 'is_first_login')
    list_filter = ('is_active', 'is_first_login')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    list_per_page = 50
    form = UserAdminForm
    actions = ('set_users_inactive', 'set_users_active')

    def get_ordering(self, request):
        return 'last_name', 'date_joined'

    def set_users_inactive(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, '{} Users have been inactive successfully.'.format(count))

    def set_users_active(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, '{} Users have been active successfully.'.format(count))

    def has_delete_permission(self, request, obj=None):
        return False


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'author', 'publication_date')
    list_filter = ('publication_date',)
    search_fields = ('title', 'author')
    list_per_page = 50

    def get_ordering(self, request):
        return ('-publication_date',)

    def has_delete_permission(self, request, obj=None):
        return False


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'comment')
    list_filter = ('timestamp',)
    search_fields = ('post', 'user')
    readonly_fields = ('post', 'user')
    list_per_page = 50

    def get_ordering(self, request):
        return ('-timestamp',)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
