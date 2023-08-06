"""Navigation Items to add to Nautobot for nautobot_dns_records."""

from nautobot.core.apps import NavMenuTab, NavMenuGroup, NavMenuItem

menu_items = (
    NavMenuTab(
        name="IPAM",
        groups=(
            NavMenuGroup(
                name="DNS",
                weight=800,
                items=(
                    NavMenuItem(
                        link="plugins:nautobot_dns_records:addressrecord_list", name="Address Records", permissions=[]
                    ),
                    NavMenuItem(link="plugins:nautobot_dns_records:txtrecord_list", name="TXT Records", permissions=[]),
                    NavMenuItem(link="plugins:nautobot_dns_records:locrecord_list", name="LOC Records", permissions=[]),
                    NavMenuItem(
                        link="plugins:nautobot_dns_records:cnamerecord_list", name="CNAME Records", permissions=[]
                    ),
                    NavMenuItem(link="plugins:nautobot_dns_records:ptrrecord_list", name="PTR Records", permissions=[]),
                    NavMenuItem(
                        link="plugins:nautobot_dns_records:sshfprecord_list", name="SSHFP Records", permissions=[]
                    ),
                    NavMenuItem(link="plugins:nautobot_dns_records:srvrecord_list", name="SRV Records", permissions=[]),
                ),
            ),
        ),
    ),
)
