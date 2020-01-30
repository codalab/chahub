from django.views.generic import DetailView

from tasks.models import Task


class TaskDetail(DetailView):
    queryset = Task.objects.all()
    template_name = 'detail_pages/task.html'
