from __future__ import absolute_import

import json
import logging

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from .models import Dataset, COPLUMN_TYPES
from .logic.preview import get_preview
from .forms import DatasetForm, DatasetUpdateForm

logger = logging.getLogger(__name__)


from cdilinker.linker.base import FIELD_CATEGORIES

FIELD_CATS = tuple((item.name, item.title) for item in FIELD_CATEGORIES)


class DatasetPreviewMixin(object):

    preview_choices = (
        ('head', 'First rows'),
        ('tail', 'Last rows'),
        ('rand', 'Random Selection')
    )


    @property
    def preview(self):

        previewer = get_preview(self.filename, self.data_format)
        result = previewer.preview('head', 25)
        return {
            "len": result['len'],
            "header": result['header'],
            "rows": result['rows'],
            "preview_choices": self.preview_choices,
        }

    def get_context_data(self, **kwargs):
        context = super(DatasetPreviewMixin, self).get_context_data(**kwargs)
        self.data_format = 'csv'
        self.filename = context['object'].url

        context['preview'] = self.preview
        return context


class DatasetListView(LoginRequiredMixin, ListView):
    model = Dataset


class DatasetCreateView(LoginRequiredMixin, CreateView):
    model = Dataset

    form_class = DatasetForm

    def get_success_url(self):
        return reverse('datasets:edit', kwargs={'name': self.object.name})

class DatasetUpdateView(LoginRequiredMixin, UpdateView):
    model = Dataset
    slug_field = 'name'
    slug_url_kwarg = 'name'

    form_class = DatasetUpdateForm
    def get_context_data(self, **kwargs):
        data = super(DatasetUpdateView, self).get_context_data(**kwargs)
        if not self.request.POST:
            data['data_types'] = self.object.data_types
            data['field_cats'] = self.object.field_cats
            data['COPLUMN_TYPES'] = COPLUMN_TYPES
            data['FIELD_CATS'] = FIELD_CATS
            previewer = get_preview(self.object.url, 'csv')
            result = previewer.preview('head', 4)
            data['columns'] = result['header']
            data['types'] = result['types']
            data['records'] = result['rows']
        return data

    def get_success_url(self):
        return reverse('datasets:list')


class DatasetDeleteView(LoginRequiredMixin, DeleteView):
    model = Dataset
    slug_field = 'name'
    slug_url_kwarg = 'name'

    form_class = DatasetUpdateForm

    def get_success_url(self):
        return reverse('datasets:list')

class DatasetDetailView(LoginRequiredMixin, DatasetPreviewMixin, DetailView):
    model = Dataset

    slug_field = 'name'
    slug_url_kwarg = 'name'


@csrf_protect
@login_required
def dataset_preview(request):

    filename = request.POST.get('filename')
    limit = request.POST.get('limit')
    criteria = request.POST.get('criteria')
    previewer = get_preview(filename, 'csv')
    result = previewer.preview(criteria, int(limit))
    data = {
        'header': result['header'],
        'rows': result['rows'],
    };

    return render(request, 'datasets/dataset_preview.html', {'preview': data})

@csrf_protect
@login_required
def dataset_header(request):
    id = request.GET.get('id', '')
    try:
        dataset = Dataset.objects.get(pk=id)
        fields = dataset.get_fields()
    except Dataset.DoesNotExist as db_err:
        logger.error('Database error. No dataset with id {0} was found.'.format(id))
        fields = None
    except ValueError as value_err:
        logger.error('Database error on fetching record data.')
        fields = None

    return HttpResponse(json.dumps({'header': fields}), content_type="application/json")
