from django import forms
from django.db import models
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

from orchestra.admin import ChangeListDefaultFilter
from orchestra.admin.filters import UsedContentTypeFilter
from orchestra.admin.utils import admin_link, admin_date
from orchestra.apps.accounts.admin import AccountAdminMixin
from orchestra.core import services
from orchestra.utils.humanize import naturaldate

from .actions import BillSelectedOrders
from .filters import ActiveOrderListFilter, BilledOrderListFilter
from .models import Plan, ContractedPlan, Rate, Service, Order, MetricStorage


class RateInline(admin.TabularInline):
    model = Rate
    ordering = ('plan', 'quantity')


class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_default', 'is_combinable', 'allow_multiple')
    list_filter = ('is_default', 'is_combinable', 'allow_multiple')
    inlines = [RateInline]


class ContractedPlanAdmin(AccountAdminMixin, admin.ModelAdmin):
    list_display = ('plan', 'account_link')
    list_filter = ('plan__name',)


class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'description', 'content_type', 'handler_type', 'num_orders', 'is_active'
    )
    list_filter = ('is_active', 'handler_type', UsedContentTypeFilter)
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('description', 'content_type', 'match', 'handler_type',
                       'is_active')
        }),
        (_("Billing options"), {
            'classes': ('wide',),
            'fields': ('billing_period', 'billing_point', 'is_fee')
        }),
        (_("Pricing options"), {
            'classes': ('wide',),
            'fields': ('metric', 'pricing_period', 'rate_algorithm',
                       'on_cancel', 'payment_style', 'tax', 'nominal_price')
        }),
    )
    inlines = [RateInline]
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        """ Improve performance of account field and filter by account """
        if db_field.name == 'content_type':
            models = [model._meta.model_name for model in services.get()]
            queryset = db_field.rel.to.objects
            kwargs['queryset'] = queryset.filter(model__in=models)
        if db_field.name in ['match', 'metric']:
            kwargs['widget'] = forms.TextInput(attrs={'size':'160'})
        return super(ServiceAdmin, self).formfield_for_dbfield(db_field, **kwargs)
    
    def num_orders(self, service):
        num = service.orders__count
        url = reverse('admin:orders_order_changelist')
        url += '?service=%i&is_active=True' % service.pk
        return '<a href="%s">%d</a>' % (url, num)
    num_orders.short_description = _("Orders")
    num_orders.admin_order_field = 'orders__count'
    num_orders.allow_tags = True
    
    def get_queryset(self, request):
        qs = super(ServiceAdmin, self).get_queryset(request)
        # Count active orders
        qs = qs.extra(select={
            'orders__count': (
                "SELECT COUNT(*) "
                "FROM orders_order "
                "WHERE orders_order.service_id = orders_service.id AND ("
                "      orders_order.cancelled_on IS NULL OR"
                "      orders_order.cancelled_on > '%s' "
                ")" % timezone.now()
            )
        })
        return qs


class OrderAdmin(AccountAdminMixin, ChangeListDefaultFilter, admin.ModelAdmin):
    list_display = (
        'id', 'service', 'account_link', 'content_object_link',
        'display_registered_on', 'display_billed_until', 'display_cancelled_on'
    )
    list_display_links = ('id', 'service')
    list_filter = (ActiveOrderListFilter, BilledOrderListFilter, 'service',)
    actions = (BillSelectedOrders(),)
    date_hierarchy = 'registered_on'
    default_changelist_filters = (
        ('is_active', 'True'),
    )
    
    content_object_link = admin_link('content_object', order=False)
    display_registered_on = admin_date('registered_on')
    display_cancelled_on = admin_date('cancelled_on')
    
    def display_billed_until(self, order):
        value = order.billed_until
        color = ''
        if value and value < timezone.now():
            color = 'style="color:red;"'
        return '<span title="{raw}" {color}>{human}</span>'.format(
            raw=escape(str(value)), color=color, human=escape(naturaldate(value)),
        )
    display_billed_until.short_description = _("billed until")
    display_billed_until.allow_tags = True
    display_billed_until.admin_order_field = 'billed_until'
    
    def get_queryset(self, request):
        qs = super(OrderAdmin, self).get_queryset(request)
        return qs.select_related('service').prefetch_related('content_object')



class MetricStorageAdmin(admin.ModelAdmin):
    list_display = ('order', 'value', 'created_on', 'updated_on')
    list_filter = ('order__service',)


admin.site.register(Plan, PlanAdmin)
admin.site.register(ContractedPlan, ContractedPlanAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(MetricStorage, MetricStorageAdmin)
