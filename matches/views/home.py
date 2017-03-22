from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic import TemplateView

from matches.forms import GenericDeleteForm
from matches.tasks import delete_all_data


class HomeView(TemplateView):
    template_name = "index.html"

class DeleteDataView(FormView):
    template_name = 'delete.html'
    form_class = GenericDeleteForm
    redirect_name = None

    def post(self, request, *args, **kwargs):
        if "save" in request.POST:
            delete_all_data()
            messages.success(self.request, "All Data Cleared")
            return super().post(request, *args, **kwargs)
        else:
            url = self.get_success_url()
            return HttpResponseRedirect(url)

    def get_success_url(self):
        success_url = reverse_lazy(
            "home",
        )

        return success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        return context