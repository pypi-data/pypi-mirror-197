# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_feedback_govuk',
 'django_feedback_govuk.migrations',
 'django_feedback_govuk.templatetags']

package_data = \
{'': ['*'],
 'django_feedback_govuk': ['static/django_feedback_govuk/*',
                           'templates/django_feedback_govuk/includes/*',
                           'templates/django_feedback_govuk/partials/*',
                           'templates/django_feedback_govuk/templates/*',
                           'templates/django_feedback_govuk/widgets/star_rating/*']}

install_requires = \
['Django>=3.2,<4.0',
 'crispy-forms-gds>=0.2.4,<0.3.0',
 'django-crispy-forms>=1.9,<2.0',
 'notifications-python-client>=8.0.0,<9.0.0']

setup_kwargs = {
    'name': 'django-feedback-govuk',
    'version': '0.1.0',
    'description': 'A Django app to gather and send internal Government staff feedback',
    'long_description': '# django-feedback\n\nA Django app to gather and send internal Government staff feedback, e.g. for open beta periods\n\n## Installation\n\n```\npip install django-feedback-govuk\n```\n\n1. Add `django-feedback` to your INSTALLED_APPS settings:\n\n```py\nINSTALLED_APPS = [\n    ...\n    \'crispy_forms\',\n    \'crispy_forms_gds\',\n    \'django_feedback_govuk\',\n]\n```\n\n2. Create a new email template in the GovUk Notify service, making sure to create a ((feedback_url)) field.\n\n> Note that ((feedback_url)) will be a link to the listing view, not an individual piece of feedback.\n\nYou\'ll need an API key and template ID from the gov.uk Notify service.\n\n3. Add the following settings to the file:\n\n```py\n# Crispy forms\nCRISPY_ALLOWED_TEMPLATE_PACKS = ["gds"]\nCRISPY_TEMPLATE_PACK = "gds"\n\n# Gov Notify\nGOVUK_NOTIFY_API_KEY="<your-api-key>"\n\n# Django Feedback GovUK\nDJANGO_FEEDBACK_GOVUK = {\n    "SERVICE_NAME": "<your-service>",\n    "FEEDBACK_NOTIFICATION_EMAIL_TEMPLATE_ID": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",\n    "FEEDBACK_NOTIFICATION_EMAIL_RECIPIENTS": ["email@example.com"],\n}\n```\n\nThe email addresses are for every recipient that should get an email when feedback is submitted.\n\n3. Build your own templates\n\nOverride the built-in templates by making new templates in your app under the\n`django_feedback_govuk/templates` path. You\'ll need templates for `submit.html`, `confirm.html`\nand `listing.html`, each of which should load its respective template tag from `feedback_submit`,\n`feedback_confirm` and `feedback_listing`.\n\nFor example:\n\n```py\n{# /your-project/templates/django_feedback_govuk/templates/submit.html #}\n{% extends "base.html" %}\n{% load feedback_tags %}\n{% block content %}\n    {% feedback_submit %}\n{% endblock content %}\n```\n\n> If you\'d like to use the templatetags without causing page loads to new views\n\n4. Add the URLs to your project\n\n```py\nfrom django_feedback_govuk import urls as feedback_urls\n\n\nurlpatterns = [\n    ...\n    path("feedback/", include(feedback_urls)),\n    ...\n]\n```\n\n5. Set up user permissions\n',
    'author': 'jafacakes2011',
    'author_email': 'cameron.lamb@digitial.trade.gov.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
