"""Forms for the nautobot dns records plugin."""
import nautobot.dcim.models
import nautobot.ipam.models
from django import forms
from django.utils.translation import gettext_lazy as _
from nautobot.extras.forms import RelationshipModelFormMixin
from nautobot.utilities.forms import BootstrapMixin, DynamicModelChoiceField

from nautobot_dns_records import models


class AddressRecordForm(BootstrapMixin, RelationshipModelFormMixin, forms.ModelForm):
    """Address Record create/edit form."""

    device = DynamicModelChoiceField(queryset=nautobot.dcim.models.Device.objects.all(), required=False)
    address = DynamicModelChoiceField(
        queryset=nautobot.ipam.models.IPAddress.objects.all(), query_params={"device_id": "$device"}
    )
    create_reverse = forms.BooleanField(label=_("Create reverse record"), required=False)

    class Meta:
        model = models.AddressRecord
        fields = ["label", "ttl", "device", "address", "status", "tags"]


class CnameRecordForm(BootstrapMixin, RelationshipModelFormMixin, forms.ModelForm):
    """CName Record create/edit form."""

    device = DynamicModelChoiceField(queryset=nautobot.dcim.models.Device.objects.all(), required=False)

    class Meta:
        model = models.CNameRecord
        fields = ["label", "ttl", "target", "device", "status", "tags"]


class LocRecordForm(BootstrapMixin, RelationshipModelFormMixin, forms.ModelForm):
    """LOC Record create/edit form."""

    device = DynamicModelChoiceField(queryset=nautobot.dcim.models.Device.objects.all(), required=False)

    class Meta:
        model = models.LocRecord
        fields = [
            "label",
            "ttl",
            "degLat",
            "minLat",
            "secLat",
            "degLong",
            "minLong",
            "secLong",
            "precision",
            "altitude",
            "device",
            "status",
            "tags",
        ]


class PtrRecordForm(BootstrapMixin, RelationshipModelFormMixin, forms.ModelForm):
    """PTR Record create/edit form."""

    device = DynamicModelChoiceField(queryset=nautobot.dcim.models.Device.objects.all(), required=False)
    address = DynamicModelChoiceField(
        queryset=nautobot.ipam.models.IPAddress.objects.all(), query_params={"device_id": "$device"}
    )

    class Meta:
        model = models.PtrRecord
        fields = ["label", "ttl", "device", "address", "status", "tags"]


class SshfpRecordForm(BootstrapMixin, RelationshipModelFormMixin, forms.ModelForm):
    """SSHFP Record create/edit form."""

    device = DynamicModelChoiceField(queryset=nautobot.dcim.models.Device.objects.all(), required=False)

    class Meta:
        model = models.SshfpRecord
        fields = ["label", "ttl", "algorithm", "hashType", "fingerprint", "device", "status", "tags"]


class TxtRecordForm(BootstrapMixin, RelationshipModelFormMixin, forms.ModelForm):
    """TXT Record create/edit form."""

    device = DynamicModelChoiceField(queryset=nautobot.dcim.models.Device.objects.all(), required=False)

    class Meta:
        model = models.TxtRecord
        fields = ["label", "ttl", "value", "device", "status", "tags"]


class SrvRecordForm(BootstrapMixin, RelationshipModelFormMixin, forms.ModelForm):
    """SRV Record create/edit form."""

    device = DynamicModelChoiceField(queryset=nautobot.dcim.models.Device.objects.all(), required=False)

    class Meta:
        model = models.SrvRecord
        fields = ["label", "ttl", "device", "priority", "weight", "port", "target", "status", "tags"]
