from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Tag, Scope, Article


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        has_main_object = 0
        for form in self.forms:
            print(form.cleaned_data)
            print(1)
            # В form.cleaned_data будет словарь с данными
            # каждой отдельной формы, которые вы можете проверить
            if len(form.cleaned_data) != 0:
                if form.cleaned_data['main_object']:
                    has_main_object += 1
            # вызовом исключения ValidationError можно указать админке о наличие ошибки
            # таким образом объект не будет сохранен,
            # а пользователю выведется соответствующее сообщение об ошибке
        if has_main_object < 1:
            raise ValidationError('Нет основного раздела')
        if has_main_object > 1:
            raise ValidationError('Больше 1 основного раздела')
        return super().clean()  # вызываем базовый код переопределяемого метода


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass