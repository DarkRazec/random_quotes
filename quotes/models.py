from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models

NULLABLE = {'blank': True, 'null': True}

class Source(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "источник"
        verbose_name_plural = "источники"

class Quote(models.Model):
    content = models.CharField(max_length=200, unique=True, verbose_name="Содержание цитаты")
    weight = models.PositiveIntegerField(default=1, verbose_name="Вес цитаты")
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, **NULLABLE, related_name="quotes")
    likes = models.ManyToManyField(AUTH_USER_MODEL, blank=True, related_name="likes")
    dislikes = models.ManyToManyField(AUTH_USER_MODEL, blank=True, related_name="dislikes")
    viewed = models.ManyToManyField(AUTH_USER_MODEL, blank=True, related_name="viewed")
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name="автор")

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "цитата"
        verbose_name_plural = "цитаты"
