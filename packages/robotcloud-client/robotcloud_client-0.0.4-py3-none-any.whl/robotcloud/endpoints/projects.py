from robotcloud.api import APIEndPointAuthenticated
from robotcloud.endpoints.organizations import APICallOrganizationProjects
from robotcloud.exceptions import BadUsageException


class APICallProjects(APIEndPointAuthenticated):
    def __init__(self, token: str, project_id: str = None):
        self.project_id = project_id
        super().__init__(token)

    def get_endpoint(self):
        if self.project_id is None:
            return "projects/"
        else:
            return f"projects/{self.project_id}"


class APICallProjectUsers(APIEndPointAuthenticated):
    def __init__(self, token: str, project_id: str):
        self.project_id = project_id
        super().__init__(token)

    def get_endpoint(self):
        return f"projects/{self.project_id}/users"


class APIEndpointProjectDevices(APIEndPointAuthenticated):
    def __init__(self, token: str, project_id: str):
        self.project_id = project_id
        super().__init__(token)

    def get_endpoint(self):
        return f"projects/{self.project_id}/devices"


def get_project(token, project_id):
    return APICallProjects(token, project_id).get()


def get_projects(token):
    return APICallProjects(token).get()


def update_project(token, project_id, new_data):
    return APICallProjects(token, project_id).put(new_data)


def get_project_users(token, project_id):
    return APICallProjectUsers(token, project_id).get()


def get_project_devices(token, project_id):
    return APIEndpointProjectDevices(token, project_id).get()


def create_project(token, data) -> dict:
    if 'organization_id' not in data or not isinstance(data['organization_id'], str):
        raise BadUsageException("")
    org_id = data['organization_id']
    data.pop('organization_id')
    return APICallOrganizationProjects(token, org_id).post(data)


def delete_project(token, project_id) -> dict:
    return APICallProjects(token, project_id).delete()
