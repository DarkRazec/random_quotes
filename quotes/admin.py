from django.contrib import admin

from quotes.models import Quote, Source

admin.site.register((Quote, Source))
