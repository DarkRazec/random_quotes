from django import forms
from django.core.exceptions import ValidationError

from quotes.models import Source, Quote


class QuoteSourceCreateForm(forms.ModelForm):
    source = forms.CharField(max_length=100, label="Источник")

    class Meta:
        model = Quote
        fields = 'content', 'weight',

    def clean_source(self):
        source_name = self.cleaned_data['source'].strip('"\' «» ')
        source_obj, created = Source.objects.get_or_create(name=source_name)

        if not created and source_obj.quotes.count() >= 3:
            raise ValidationError("У данного источника уже есть 3 цитаты")
        self.cleaned_data['source_obj'] = source_obj
        return source_name

    def clean_quote(self):
        return self.cleaned_data['quote'].strip('"\' «» ')

    def clean_weight(self):
        weight = self.cleaned_data['weight']
        if 0 < weight < 11:
            return weight
        raise ValidationError("Значение веса должно быть в диапазоне от 1 до 10")

    def save(self, commit=True):
        quote = super().save()
        quote.source = self.cleaned_data['source_obj']
        quote.save()
        return quote