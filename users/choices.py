#!/usr/bin/env python
from django.utils.translation import ugettext_lazy as _

ACCOUNT_TYPE = (
        ('IND', _('Individual')),
        ('BIZ', _('Business')),
        ('EDU', _('Education')),
    )

GENDER_CHOICES = (
        ('N', _('N/A')),
        ('M', _('Male')),
        ('F', _('Female')),
        ('O', _('Other')),

    )

EDUCATION_CHOICES = (
        ('NA', _('N/A')),
        ('HS', _('Diploma')),
        ('AD', _('Associates')),
        ('BD', _('Bachelors')),
        ('MD', _('Masters')),
        ('PH', _('Doctorate')),
    )