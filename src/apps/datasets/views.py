from django.views.generic import DetailView

from datasets.models import Data


class DatasetDetail(DetailView):
    queryset = Data.objects.all()
    template_name = 'detail_pages/dataset.html'
