import json

from django.core.mail import mail_admins
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader, Context
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@require_POST
def report(request):
    """
    Accept a Content Security Policy violation report and forward
    the report via email to ADMINS.

    """

    try:
        violation = json.loads(request.raw_post_data)['csp-report']
    except Exception:
        return HttpResponseBadRequest()

    data = {}
    for key in violation:
        data[key.replace('-', '_')] = violation[key]

    c = Context(data)
    t = loader.get_template('csp/email/report.ltxt')
    body = t.render(c)

    mail_admins('CSP Violation', body)
    return HttpResponse()
