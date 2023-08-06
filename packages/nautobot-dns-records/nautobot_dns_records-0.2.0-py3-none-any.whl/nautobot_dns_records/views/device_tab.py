"""Add a tab to the device object view."""
from nautobot.core.views import generic
from nautobot.dcim.models import Device

from nautobot_dns_records.models import (
    AddressRecord,
    PtrRecord,
    TxtRecord,
    CNameRecord,
    LocRecord,
    SshfpRecord,
    SrvRecord,
)
from nautobot_dns_records.tables import (
    AddressRecordTable,
    PtrRecordTable,
    TxtRecordTable,
    CnameRecordTable,
    LocRecordTable,
    SshfpRecordTable,
    SrvRecordTable,
)


class DeviceRecordsTab(generic.ObjectView):
    """Display all dns records for a device."""

    queryset = Device.objects.all()
    template_name = "nautobot_dns_records/tab_device_records.html"

    def get_extra_context(self, request, instance):  # pylint: disable-msg=too-many-locals
        """Returns all dns records related to a device."""
        addressrecords = AddressRecord.objects.filter(address__interface__device=instance).all()
        addressrecords_table = AddressRecordTable(data=addressrecords, user=request.user, orderable=False)
        ptrrecords = PtrRecord.objects.filter(address__interface__device=instance).all()
        ptrrecords_table = PtrRecordTable(data=ptrrecords, user=request.user, orderable=False)
        txtrecords = TxtRecord.objects.filter(device=instance).all()
        txtrecords_table = TxtRecordTable(data=txtrecords, user=request.user, orderable=False)
        cnamerecords = CNameRecord.objects.filter(device=instance).all()
        cnamerecords_table = CnameRecordTable(data=cnamerecords, user=request.user, orderable=False)
        locrecords = LocRecord.objects.filter(device=instance).all()
        locrecords_table = LocRecordTable(data=locrecords, user=request.user, orderable=False)
        sshfprecords = SshfpRecord.objects.filter(device=instance).all()
        sshfprecords_table = SshfpRecordTable(data=sshfprecords, user=request.user, orderable=False)
        srvrecords = SrvRecord.objects.filter(device=instance).all()
        srvprecords_table = SrvRecordTable(data=srvrecords, user=request.user, orderable=False)

        extra_context = {
            "addressrecords_table": addressrecords_table,
            "ptrrecords_table": ptrrecords_table,
            "txtrecords_table": txtrecords_table,
            "cnamerecords_table": cnamerecords_table,
            "locrecords_table": locrecords_table,
            "sshfprecords_table": sshfprecords_table,
            "srvrecords_table": srvprecords_table,
        }
        return {
            **extra_context,
            **super().get_extra_context(request, instance),
        }
