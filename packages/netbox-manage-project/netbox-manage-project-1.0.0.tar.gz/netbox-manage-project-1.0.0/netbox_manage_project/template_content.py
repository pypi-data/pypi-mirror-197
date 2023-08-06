from extras.plugins import PluginTemplateExtension
from .models import Project
# from dcim.models import Device
# from tenancy.models import Contact
# from ipam.models import IPAddress
# from virtualization.models import VirtualMachine

class ProjectInfoExtension(PluginTemplateExtension):
    def left_page(self):
        object = self.context.get('object')
        project = Project.objects.filter(**{self.kind:object})
        return self.render('netbox_manage_project/inc/project_info.html', extra_context={
            'project': project,
        })


class DeviceProjectInfo(ProjectInfoExtension):
    model = 'dcim.device'
    kind = 'devices'


class IPAddressProjectInfo(ProjectInfoExtension):
    model = 'ipam.ipaddress'
    kind = 'ipaddress'


class VirtualMachineProjectInfo(ProjectInfoExtension):
    model = 'virtualization.virtualmachine'
    kind = 'virtualmachine'


class ContactProjectInfo(ProjectInfoExtension):
    model = 'tenancy.contact'
    kind = 'contact'


template_extensions = (
    DeviceProjectInfo,
    IPAddressProjectInfo,
    VirtualMachineProjectInfo,
    ContactProjectInfo,
)