from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse


from bboard.models import Ad, Rubric
from bboard.forms import AdForm

import logging

logger = logging.getLogger()


def index(request):
    logger.error('Test!')
    logger.debug('Test1')
    logger.warning('Test')
    logger.info('TestInfo')
    logger.critical('TestCritical')
    ads = Ad.objects.order_by('-published')
    context = {'ads': ads}
    return TemplateResponse(request, 'bboard/index.html', context=context)


class AdCreateView(CreateView):
    template_name = 'bboard/create.html'
    form_class = AdForm
    success_url = reverse_lazy('bboard:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


def add_and_save(request):

    if request.method == 'POST':
        ad = AdForm(request.POST)
        if ad.is_valid():
            ad.save()
            return HttpResponseRedirect(reverse('bboard:index'))
        else:
            context = {'form': ad}
            return render(request, 'bboard/create.html', context)

    else:
        ad = AdForm()
        context = {'form': ad}
        return render(request, 'bboard/create.html', context)


class AdDetailView(DetailView):
    model = Ad

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class AdListView(ListView):
    model = Ad
    template_name = 'bboard/index.html'
    context_object_name = 'ads'


class AdEditView(UpdateView):
    model = Ad
    form_class = AdForm
    success_url = reverse_lazy('bboard:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class AdDeleteView(DeleteView):
    model = Ad
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


def detail_view(request, pk):
    print(pk)
    return HttpResponseRedirect(reverse('bboard:delete', kwargs={'pk': 6}))
