from django.conf import settings
from django.contrib import admin

from transaction.forms import CommentInlineFormset, TransactionModelForm
from transaction.models import Transaction, Comment


class CommentInline(admin.TabularInline):

    model = Comment
    readonly_fields = ('author', 'timestamp')
    extra = 1
    max_num = 10
    can_delete = True
    formset = CommentInlineFormset

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(CommentInline, self).get_formset(request, obj, **kwargs)
        formset.request = request
        return formset


class TransactionAdmin(admin.ModelAdmin):

    form = TransactionModelForm

    def sender_url(self, obj):
        path = settings.API_BASE_URL + 'admin/account/beamprofile'
        return '<a href="{}/{}/">{} {}</a>'.format(
            path, obj.sender.profile.id, obj.sender.first_name, obj.sender.last_name)

    sender_url.allow_tags = True
    sender_url.short_description = 'sender'

    def recipient_url(self, obj):
        path = settings.API_BASE_URL + 'admin/recipient/recipient'
        return '<a href="{}/{}/">{} {} ({})</a>'.format(
            path, obj.recipient.id, obj.recipient.first_name,
            obj.recipient.last_name, obj.recipient.id
        )

    recipient_url.allow_tags = True
    recipient_url.short_description = 'recipient'

    def exchange_rate_url(self, obj):
        path = settings.API_BASE_URL + 'admin/pricing/exchangerate'
        return '<a href="{}/{}/">{}</a>'.format(
            path, obj.exchange_rate.id, obj.exchange_rate.usd_ghs)

    def sender_email(self, obj):
        return obj.sender.email

    sender_email.allow_tags = True
    sender_email.short_description = 'sender email'

    def recipient_name(self, obj):
        return '{} {}'.format(obj.recipient.first_name, obj.recipient.last_name)

    recipient_name.allow_tags = True
    recipient_name.short_description = 'recipient name'

    readonly_fields = (
        'sender_url', 'recipient_url', 'exchange_rate_url', 'transaction_type',
        'reference_number', 'last_changed', 'additional_info'
    )

    read_and_write_fields = ()

    fieldsets = (
        (None, {
            'fields': ('sender_url', 'recipient_url', 'transaction_type', 'reference_number',
                       'state', 'additional_info', 'last_changed')
        }),
        ('Pricing', {
            'fields': ('exchange_rate_url', 'cost_of_delivery_usd',
                       'cost_of_delivery_ghs', 'service_charge')
        })
    )

    list_display = (
        'id', 'sender_email', 'recipient_name', 'transaction_type', 'reference_number', 'state'
    )

    list_filter = ('state',)

    search_fields = ('id', 'reference_number')

    list_per_page = 15

    inlines = (CommentInline, )

    def save_model(self, request, obj, form, change):

        if 'state' in form.changed_data:
            obj.add_status_change(
                author=request.user,
                comment=getattr(obj, 'state')
            )

        if 'cost_of_delivery_ghs' in form.changed_data:
            obj.cost_of_delivery_usd = getattr(obj, 'cost_of_delivery_ghs') / obj.exchange_rate.usd_ghs

        elif 'cost_of_delivery_usd' in form.changed_data:
            obj.cost_of_delivery_ghs = getattr(obj, 'cost_of_delivery_usd') * obj.exchange_rate.usd_ghs

        obj.save()

admin.site.register(Transaction, TransactionAdmin)
