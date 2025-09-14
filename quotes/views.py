from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, TemplateView, CreateView, DetailView

from quotes.forms import QuoteSourceCreateForm
from quotes.models import Quote
from quotes.services import get_weighted_quote_id, get_sorted_quotes, add_remove_relation


class HomepageView(TemplateView):
    template_name = "quotes/homepage.html"
    extra_context = {
        "title": "Цитатник"
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quote_id'] = get_weighted_quote_id()
        return context


class QuoteView(DetailView):
    model = Quote
    template_name = "quotes/detail.html"
    extra_context = {
        "title": "Вот цитата для Вас:",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next_quote_id'] = get_weighted_quote_id()
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.is_authenticated:
            self.object.viewed.add(request.user)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"{reverse_lazy('users:login')}?next={request.path}")
        add_remove_relation(self.get_object(), request.user, request.POST.get('value'))
        return redirect(request.path)


class QuoteListView(ListView):
    model = Quote
    paginate_by = 10
    template_name = "quotes/list.html"
    extra_context = {
        "title": "Все цитаты"
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        querydict = self.request.GET.copy()
        querydict.pop('page', None)
        context['querystring'] = querydict.urlencode()
        return context

    def get_queryset(self):
        qs_objects = Quote.objects.annotate(
            likes_count=Count("likes", distinct=True),
            viewed_count=Count("viewed", distinct=True)
        )
        sort_method = self.request.GET.get("sort")
        return get_sorted_quotes(qs_objects, sort_method)


class QuoteCreateView(LoginRequiredMixin, CreateView):
    form_class = QuoteSourceCreateForm
    template_name = "quotes/create.html"
    extra_context = {
        "title": "Создание цитаты"
    }
    success_url = reverse_lazy("quotes:homepage")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next') or reverse_lazy('quotes:homepage')
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class QuoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Quote
    template_name = "quotes/create.html"
    fields = "weight",
    extra_context = {
        "title": "Изменить вес цитаты",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next') or reverse_lazy('quotes:homepage')
        return context

    def get_success_url(self):
        return reverse_lazy('quotes:detail', args=[self.kwargs.get('pk')])
