import re

from django.core import validators
from django.utils import six
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _


@deconstructible
class ASCIIUsernameValidator(validators.RegexValidator):
    regex = r'^[\u4e00-\u9fa5_a-zA-Z0-9]+$'
    message = _(
        'Enter a valid username. This value may contain only Chinese, English letters, '
        'numbers, and @/./+/-/_ characters.'
    )
    flags = re.ASCII if six.PY3 else 0


@deconstructible
class UnicodeUsernameValidator(validators.RegexValidator):
    regex = r'^[\u4e00-\u9fa5_a-zA-Z0-9]+$'
    message = _(
        'Enter a valid username. This value may contain only Chinese, English letters, '
        'numbers, and @/./+/-/_ characters.'
    )
    flags = re.UNICODE if six.PY2 else 0