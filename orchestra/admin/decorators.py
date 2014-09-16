from functools import wraps, partial

from django.contrib import messages
from django.contrib.admin import helpers
from django.template.response import TemplateResponse 
from django.utils.decorators import available_attrs
from django.utils.encoding import force_text


def admin_field(method):
    """ Wraps a function to be used as a ModelAdmin method field """
    def admin_field_wrapper(*args, **kwargs):
        """ utility function for creating admin links """
        kwargs['field'] = args[0] if args else ''
        kwargs['order'] = kwargs.get('order', kwargs['field'])
        kwargs['popup'] = kwargs.get('popup', False)
        kwargs['short_description'] = kwargs.get('short_description',
                kwargs['field'].split('__')[-1].replace('_', ' ').capitalize())
        admin_method = partial(method, **kwargs)
        admin_method.short_description = kwargs['short_description']
        admin_method.allow_tags = True
        admin_method.admin_order_field = kwargs['order']
        return admin_method
    return admin_field_wrapper


def action_with_confirmation(action_name=None, extra_context={},
                             template='admin/orchestra/generic_confirmation.html'):
    """ 
    Generic pattern for actions that needs confirmation step
    If custom template is provided the form must contain:
    <input type="hidden" name="post" value="generic_confirmation" />
    """
    def decorator(func, extra_context=extra_context, template=template, action_name=action_name):
        @wraps(func, assigned=available_attrs(func))
        def inner(modeladmin, request, queryset, action_name=action_name):
            # The user has already confirmed the action.
            if request.POST.get('post') == "generic_confirmation":
                stay = func(modeladmin, request, queryset)
                if not stay:
                    return
            
            opts = modeladmin.model._meta
            app_label = opts.app_label
            action_value = func.__name__
            
            if len(queryset) == 1:
                objects_name = force_text(opts.verbose_name)
            else:
                objects_name = force_text(opts.verbose_name_plural)
            if not action_name:
                action_name = func.__name__
            context = {
                "title": "Are you sure?",
                "content_message": "Are you sure you want to %s the selected %s?" %
                                    (action_name, objects_name),
                "action_name": action_name.capitalize(),
                "action_value": action_value,
                "display_objects": queryset,
                'queryset': queryset,
                "opts": opts,
                "app_label": app_label,
                'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
            }
            
            context.update(extra_context)
            
            # Display the confirmation page
            return TemplateResponse(request, template,
                context, current_app=modeladmin.admin_site.name)
        return inner
    return decorator
