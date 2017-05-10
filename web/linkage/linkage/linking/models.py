from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField

from linkage.datasets.models import Dataset


PROJECT_TYPES = (
    ('DEDEUP', 'De-Duplication'),
    ('LINK', 'Data Linkage')
)

LINKING_METHODS = (
    ('DTR', 'Deterministic'),
    ('PRB', 'Probabilistic'),
)

LINKING_RELATIONSHIPS = (
    ('1T1', 'One to One'),
    ('1TM', 'One to Many'),
    ('MT1', 'Many to One'),
)

BLOKING_COMPARISONS = (
    ('EXACT', 'Exact'),
    ('SOUNDEX', 'Soundex'),
    ('NYSIIS', 'New York State Identification and Intelligence System'),
)

PROJECT_STATUS = (
    ('DRAFT', 'DRAFT'),
    ('READY', 'Ready'),
    ('RUNNING', 'In Progress'),
    ('COMPLETED', 'Completed'),
    ('FAILED', 'Failed'),
)

class LinkingProject(models.Model):
    name = models.CharField(_('Lnking project name'), unique=True, max_length=255)
    type = models.CharField(_('Project Type'), max_length=10, choices=PROJECT_TYPES, default='LINK')
    description = models.TextField(_('Linking Project description'), blank=True)
    relationship_type = models.CharField(_('Linking Relationship type'), max_length=3, choices=LINKING_RELATIONSHIPS,
                                         default='1T1')
    linked_url = models.URLField(_('Linked output file'))
    matched_url = models.URLField(_('Matched but not linked records file'))
    results_file = models.CharField(_('Project summary file'), max_length=255, blank=True)
    datasets = models.ManyToManyField(Dataset, through='LinkingDataset')
    status = models.CharField(_('Project Status'), max_length=10, choices=PROJECT_STATUS, default='DRAFT')
    comments = models.TextField(_('Comments'), blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("linking:edit", kwargs={"name": self.name})

class LinkingDataset(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    link_project = models.ForeignKey(LinkingProject, on_delete=models.CASCADE)
    link_seq = models.IntegerField()
    columns = JSONField(blank=True, null=True)

    class Meta:
        ordering = ['link_seq']


@python_2_unicode_compatible
class LinkingStep(models.Model):
    seq = models.IntegerField()
    blocking_schema = JSONField()
    linking_schema = JSONField()
    group = models.BooleanField(_('Dedup Entity Group Flag'), default=True)
    linking_project = models.ForeignKey(LinkingProject, related_name='steps', on_delete=models.CASCADE)
    linking_method = models.CharField(_('Linking Method'), max_length=3, choices=LINKING_METHODS, default='DTR')

    def __str__(self):
        return 'Linking step {0} of linking project {}.'.format(self.seq, self.linking_project)

    class Meta:
        ordering = ['seq']
