from google.cloud import compute_v1

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


def delete_instance_group(name, callback=None, project=None, zone=None):
    try:
        if not project:
            project = PROJECT
        if not zone:
            zone = ZONE
        _check_project_zone_set(project, zone)

        request = compute_v1.DeleteInstanceGroupManagerRequest()
        request.instance_group_manager = name
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


def _check_project_zone_set(project, zone):
    if project == "":
        raise Exception("Project not set, please specify project or set Deployer.PROJECT")
    if zone == "":
        raise Exception("Zone not set, please specify zone or set Deployer.ZONE")
