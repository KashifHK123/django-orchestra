import textwrap

from django.contrib import messages
from django.core.mail import mail_admins
from django.core.urlresolvers import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import ungettext, ugettext_lazy as _


def get_backends_help_text(backends):
    help_texts = {}
    for backend in backends:
        context = {
            'model': backend.model,
            'related_models': str(backend.related_models),
            'script_executable': backend.script_executable,
            'script_method': str(backend.script_method),
            'function_method': str(backend.script_method),
            'actions': ', '.join(backend.actions),
        }
        help_text = textwrap.dedent("""
            - Model: '%(model)s'<br>
            - Related models: %(related_models)s<br>
            - Script executable: %(script_executable)s<br>
            - Script method: %(script_method)s<br>
            - Function method: %(function_method)s<br>
            - Actions: %(actions)s<br>"""
        ) % context
        docstring = backend.__doc__
        if docstring:
            try:
                docstring = (docstring % backend.format_docstring).strip().splitlines()
            except TypeError as e:
                raise TypeError(str(backend) + str(e))
            help_text += '<br>' + '<br>'.join(docstring)
        help_texts[backend.get_name()] = help_text
    return help_texts


def send_report(method, args, log):
    server = args[0]
    backend = method.__self__.__class__.__name__
    subject = '[Orchestra] %s execution %s on %s'  % (backend, log.state, server)
    separator = "\n%s\n\n" % ('~ '*40,)
    message = separator.join([
        "[EXIT CODE] %s" % log.exit_code,
        "[STDERR]\n%s" % log.stderr,
        "[STDOUT]\n%s" % log.stdout,
        "[SCRIPT]\n%s" % log.script,
        "[TRACEBACK]\n%s" % log.traceback,
    ])
    html_message = '\n\n'.join([
        '<h4 style="color:#505050;">Exit code %s</h4>' % log.exit_code,
        '<h4 style="color:#505050;">Stderr</h4>'
            '<pre style="margin-left:20px;font-size:11px">%s</pre>' % escape(log.stderr),
        '<h4 style="color:#505050;">Stdout</h4>'
            '<pre style="margin-left:20px;font-size:11px">%s</pre>' % escape(log.stdout),
        '<h4 style="color:#505050;">Script</h4>'
            '<pre style="margin-left:20px;font-size:11px">%s</pre>' % escape(log.script),
        '<h4 style="color:#505050;">Traceback</h4>'
            '<pre style="margin-left:20px;font-size:11px">%s</pre>' % escape(log.traceback),
    ])
    mail_admins(subject, message, html_message=html_message)


def message_user(request, logs):
    total, successes = 0, 0
    ids = []
    for log in logs:
        total += 1
        if log.state != log.EXCEPTION:
            # EXCEPTION logs are not stored on the database
            ids.append(log.pk)
        if log.state == log.SUCCESS:
            successes += 1
    errors = total-successes
    if len(ids) == 1:
        url = reverse('admin:orchestration_backendlog_change', args=ids)
        href = '<a href="{}">backends</a>'.format(url)
    elif len(ids) > 1:
        url = reverse('admin:orchestration_backendlog_changelist')
        url += '?id__in=%s' % ','.join(map(str, ids))
        href = '<a href="{}">backends</a>'.format(url)
    else:
        href = ''
    if errors:
        msg = ungettext(
            _('{errors} out of {total} {href} has fail to execute.'),
            _('{errors} out of {total} {href} have fail to execute.'),
            errors)
        messages.error(request, mark_safe(msg.format(errors=errors, total=total, href=href)))
    else:
        msg = ungettext(
            _('{total} {href} has been executed.'),
            _('{total} {href} have been executed.'),
            total)
        messages.success(request, mark_safe(msg.format(total=total, href=href)))
