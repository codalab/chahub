from django.views.generic import DetailView

from competitions.models import Competition


class CompetitionDetail(DetailView):
    queryset = Competition.objects.all()
    template_name = 'detail_pages/competition.html'
