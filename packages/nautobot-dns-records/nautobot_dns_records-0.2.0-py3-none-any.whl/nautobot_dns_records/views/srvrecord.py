"""Views for the srv record model."""

from nautobot.core.views import generic

from nautobot_dns_records import models, forms
from nautobot_dns_records import tables


class SrvRecordsListView(generic.ObjectListView):
    """List all Srv Records."""

    queryset = models.SrvRecord.objects.all()
    table = tables.SrvRecordTable
    action_buttons = ("add",)


class SrvRecordView(generic.ObjectView):
    """Show a Address Record."""

    queryset = models.SrvRecord.objects.all()


class SrvRecordEditView(generic.ObjectEditView):
    """Edit an address record."""

    queryset = models.SrvRecord.objects.all()
    model_form = forms.SrvRecordForm


class SrvRecordDeleteView(generic.ObjectDeleteView):
    """Delete an address record."""

    queryset = models.SrvRecord.objects.all()
