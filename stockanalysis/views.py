from django.shortcuts import render
from dal import autocomplete
from .models import Stock

# Create your views here.

def stocks(request):
    return render(request, 'stockanalysis/stocks.html')


class StockAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Stock.objects.all()
        
        if self.q:
            print('entered keyword=>', self.q)
            qs = qs.filter(name__istartswith=self.q)
            print('result==>', qs)

        return qs
    
