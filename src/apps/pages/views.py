from django.views.generic import TemplateView


class CompetitionFormView(TemplateView):
    template_name = 'competitions/form.html'
