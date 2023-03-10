from django.contrib import admin
from functools import update_wrapper

from django.utils.html import format_html

from django.db.models import Q, Subquery
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.http import urlencode
from django.views.decorators.csrf import csrf_protect


from .models import Category


csrf_protect_m = method_decorator(csrf_protect)


@admin.register(Category)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    fields = ('name', 'parent')
    list_display = ('category_show_link', 'category_update_link', 'add_into_category_link')

    def add_into_category_link(self, obj):
        url = reverse(f"admin:menu_category_add") + "?" + urlencode({"parent": f"{obj.id}"})
        return format_html('<a href="{}">добавить в {}</a>', url, obj.name)

    def category_update_link(self, obj):
        url = reverse(f"admin:menu_category_change", args=[obj.id])
        return format_html('<a href="{}">редактировать {}</a>', url, obj.name)

    def category_show_link(self, obj):
        url = reverse("admin:menu_category_changelist") + f'{obj.id}'
        return format_html('<a href="{}">{}</a>', url, obj)

    category_show_link.short_description = "Развернуть"
    category_update_link.short_description = "Редактировать"
    add_into_category_link.short_description = "Добавить в"

    def get_queryset(self, request):
        if hasattr(request, 'showing_object_id'):
            category = self.model._default_manager.filter(pk=request.showing_object_id)

            qs = self.model._default_manager.filter(
                Q(menu_name=Subquery(category.values('menu_name')[:1]))
                &
                (Q(left__lte=Subquery(category.values('left')[:1]),
                   right__gte=Subquery(category.values('right')[:1]), )
                 |
                 Q(parent__in=self.model._default_manager.filter(
                     left__lte=Subquery(category.values('left')[:1]),
                     right__gte=Subquery(category.values('right')[:1])))
                 )
                |
                Q(parent=None)
            )
            return qs
        else:
            qs = self.model._default_manager.get_queryset().filter(parent=None)
        return qs

    def get_urls(self):
        from django.urls import path

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        return [
            path("", wrap(self.changelist_view), name="%s_%s_changelist" % info),
            path("add/", wrap(self.add_view), name="%s_%s_add" % info),
            path(
                "<path:object_id>/history/",
                wrap(self.history_view),
                name="%s_%s_history" % info,
            ),
            path(
                "<path:object_id>/delete/",
                wrap(self.delete_view),
                name="%s_%s_delete" % info,
            ),
            path(
                "<path:object_id>/change/",
                wrap(self.change_view),
                name="%s_%s_change" % info,
            ),
            # For backwards compatibility (was the change url before 1.9)
            path(
                "<path:object_id>/",
                wrap(self.changelist_view), name="%s_%s_changelist" % info
            ),
        ]

    @csrf_protect_m
    def changelist_view(self, request, extra_context=None, object_id=None):
        if object_id:
            request.showing_object_id = object_id
        return super(AuthorAdmin, self).changelist_view(request, extra_context)




