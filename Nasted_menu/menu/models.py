from django.db import models
from django.db.models import Q, Subquery


class Category(models.Model):
    name = models.CharField(verbose_name=u'Заголовок', max_length=255)
    left = models.IntegerField(blank=True, null=True)
    right = models.IntegerField(blank=True, null=True)
    parent = models.ForeignKey('self', verbose_name=u'Родительская категория', blank=True, null=True,
                               related_name='children', on_delete=models.CASCADE)
    level = models.IntegerField(blank=True, null=True)
    menu_name = models.CharField(verbose_name=u'Название меню', max_length=255, blank=True, null=True)

    def __unicode__(self):
        level = self.level if self.level else 1
        i = u'| ' if level > 1 else ''
        return (u'|--' * (level - 1)) + i + self.name

    def __str__(self):
        level = self.level if self.level else 1
        i = '| ' if level > 1 else ''
        return ('|--' * (level - 1)) + i + self.name

    class Meta:
        ordering = ('menu_name', 'left',)

    def save(self, *args, **kwargs):
        if self.parent:
            self.menu_name = self.parent.menu_name
        else:
            self.menu_name = self.name
        super(Category, self).save(*args, **kwargs)

        self.set_mptt()

    def set_mptt(self, left=1, parent=None, level=1):
        for category in type(self).objects.filter(parent=parent, menu_name=self.menu_name).order_by('name'):
            children = category.children.all()
            children_count = 0
            while children:
                next_children = []
                for child in children:
                    children_count += 1
                    if child.children.exists():
                        next_children += child.children.all()
                children = next_children

            data = {
                'level': level,
                'left': left,
                'right': left + (children_count * 2) + 1
            }

            type(self).objects.filter(id=category.id).update(**data)

            left = data['right'] + 1
            self.set_mptt(left=data['left'] + 1, parent=category.id, level=data['level'] + 1)

    @staticmethod
    def get_menu(pk):
        category = Category.objects.filter(pk=pk)
        result = Category.objects.filter(
            Q(menu_name=Subquery(category.values('menu_name')[:1]))
            &
            (
                    Q(left__lte=Subquery(category.values('left')[:1]),
                      right__gte=Subquery(category.values('right')[:1]),)
                    |
                    Q(parent__in=Category.objects.filter(
                        left__lte=Subquery(category.values('left')[:1]),
                        right__gte=Subquery(category.values('right')[:1]),))
            )
        )
        return result
