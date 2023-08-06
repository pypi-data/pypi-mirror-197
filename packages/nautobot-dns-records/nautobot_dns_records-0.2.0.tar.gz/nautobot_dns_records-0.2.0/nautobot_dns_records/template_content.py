"""Modifies build in nautobot templates."""
from django.urls import reverse
from nautobot.extras.plugins import PluginTemplateExtension


class DeviceExtraTabs(PluginTemplateExtension):
    """Add extra device tabs."""

    model = "dcim.device"

    def detail_tabs(self):
        """Add tabs to the device detail view."""
        return [
            {
                "title": "DNS Records",
                "url": reverse("plugins:nautobot_dns_records:device_records", kwargs={"pk": self.context["object"].pk}),
            },
        ]

    def buttons(self):
        """Add additional buttons to the device detail view."""
        return ""

    def full_width_page(self):
        """Add additional full width content to the device detail view."""
        return ""

    def left_page(self):
        """Add additional content to the left page of the device detail view."""
        return ""

    def right_page(self):
        """Add additional content to the left page of the device detail view."""
        return ""


template_extensions = [
    DeviceExtraTabs,
]
