from google.cloud import compute_v1
import re

# Global vars
PROJECT = ""
ZONE = ""


def deploy_instance_group(name, instance_base_name, template_url, size, callback=None, project=None, zone=None):
    try:
        if not project:
            project = PROJECT
        if not zone:
            zone = ZONE
        _check_project_zone_set(project, zone)

        # Setup instance group
        instance_group = compute_v1.InstanceGroupManager()
        instance_group.name = name
        instance_group.description = "Simple GCD"
        instance_group.base_instance_name = instance_base_name
        instance_group.instance_template = template_url
        instance_group.target_size = size

        # Create reqeust
        request = compute_v1.InsertInstanceGroupManagerRequest()
        request.project = project
        request.zone = zone
        request.instance_group_manager_resource = instance_group

        # Send request
        instance_group_manager_client = compute_v1.InstanceGroupManagersClient()
        operation = instance_group_manager_client.insert(request=request)

        if callback:
            operation.add_done_callback(callback)

        operation.result()

    except Exception as e:
        print("Error creating instance group: " + str(e))
        return False


def delete_instance_group(instance_group, callback=None, project=None, zone=None):
    try:
        if not project:
            project = PROJECT
        if not zone:
            zone = ZONE
        _check_project_zone_set(project, zone)

        # Create request
        request = compute_v1.DeleteInstanceGroupManagerRequest()
        request.instance_group_manager = instance_group
        request.project = project
        request.zone = zone

        # Send request
        instance_group_manager_client = compute_v1.InstanceGroupManagersClient()
        operation = instance_group_manager_client.delete(request=request)

        if callback:
            operation.add_done_callback(callback)

        operation.result()

    except Exception as e:
        print("Error deleting instance group: " + str(e))
        return False


def resize_instance_group(instance_group, size, callback=None, project=None, zone=None):
    try:
        if not project:
            project = PROJECT
        if not zone:
            zone = ZONE
        _check_project_zone_set(project, zone)

        # Create request
        request = compute_v1.ResizeInstanceGroupManagerRequest()
        request.instance_group_manager = instance_group
        request.size = size
        request.project = project
        request.zone = zone

        # Send request
        instance_group_manager_client = compute_v1.InstanceGroupManagersClient()
        operation = instance_group_manager_client.resize(request=request)

        if callback:
            operation.add_done_callback(callback)

        operation.result()

    except Exception as e:
        print("Error resizing instance group: " + str(e))
        return False


def list_instances_in_group(instance_group, project=None, zone=None):
    try:
        if not project:
            project = PROJECT
        if not zone:
            zone = ZONE
        _check_project_zone_set(project, zone)

        # Create request
        request = compute_v1.ListManagedInstancesInstanceGroupManagersRequest()
        request.instance_group_manager = instance_group
        request.project = project
        request.zone = zone

        instance_group_manager_client = compute_v1.InstanceGroupManagersClient()
        instances = instance_group_manager_client.list_managed_instances(request=request)

        instance_dict_array = []
        for instance in instances:
            instance_name = re.sub(".*/", "", instance.instance)
            ip = get_instance_nat_ip(instance_name)
            instance_dict_array.append(dict(name=instance_name, url=instance.instance, state=instance.instance_status, ip=ip))

        return instance_dict_array

    except Exception as e:
        print("Error listing instance group: " + str(e))
        return False


def get_instance_nat_ip(instance_name, project=None, zone=None):
    try:
        if not project:
            project = PROJECT
        if not zone:
            zone = ZONE
        _check_project_zone_set(project, zone)

        # Create request
        request = compute_v1.GetInstanceRequest()
        request.instance = instance_name
        request.project = project
        request.zone = zone

        instance_client = compute_v1.InstancesClient()
        instance = instance_client.get(request=request)

        return instance.network_interfaces[0].access_configs[0].nat_i_p  # Public ip

    except Exception as e:
        print("Error listing vm instance: " + str(e))
        return False


def delete_instances(instance_group, instances, callback=None, project=None, zone=None):
    try:
        if not project:
            project = PROJECT
        if not zone:
            zone = ZONE
        _check_project_zone_set(project, zone)

        # Create request
        request = compute_v1.InstanceGroupManagersDeleteInstancesRequest()
        request.instances = instances

        del_request = compute_v1.DeleteInstancesInstanceGroupManagerRequest()
        del_request.instance_group_manager = instance_group
        del_request.instance_group_managers_delete_instances_request_resource = request
        del_request.project = project
        del_request.zone = zone

        instance_group_manager_client = compute_v1.InstanceGroupManagersClient()
        operation = instance_group_manager_client.delete_instances(request=del_request)

        if callback:
            operation.add_done_callback(callback)

        operation.result()

    except Exception as e:
        print("Error deleting vm instance: " + str(e))
        return False

def _check_project_zone_set(project, zone):
    if project == "":
        raise Exception("Project not set, please specify project or set Deployer.PROJECT")
    if zone == "":
        raise Exception("Zone not set, please specify zone or set Deployer.ZONE")
