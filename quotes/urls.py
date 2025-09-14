from django.urls import path

from quotes.apps import QuotesConfig
from quotes.views import QuoteView, QuoteCreateView, QuoteUpdateView, HomepageView, QuoteListView

app_name = QuotesConfig.name

urlpatterns = [
    path("", HomepageView.as_view(), name="homepage"),
    path("list/", QuoteListView.as_view(), name="list"),
    path("<int:pk>/", QuoteView.as_view(), name="detail"),
    path("create/", QuoteCreateView.as_view(), name="create"),
    path("<int:pk>/update/", QuoteUpdateView.as_view(), name="update")
]