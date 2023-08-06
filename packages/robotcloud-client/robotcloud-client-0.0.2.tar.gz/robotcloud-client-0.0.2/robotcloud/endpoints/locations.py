from robotcloud.api import APIEndPointAuthenticated
from robotcloud.exceptions import BadUsageException


class APICallLocation(APIEndPointAuthenticated):
    def __init__(self, token: str, location_id: str):
        self.location_id = location_id
        super().__init__(token)

    def get_endpoint(self):
        return f"locations/{self.location_id}"


class ProjectLocationsEndpoint(APIEndPointAuthenticated):
    def __init__(self, token: str, project_id: str):
        self.project_id = project_id
        super().__init__(token)

    def get_endpoint(self):
        return f"projects/{self.project_id}/locations"


def create_location(token, data: dict):
    if 'project_id' not in data or not isinstance(data['project_id'], str):
        raise BadUsageException("")

    project_id = data['project_id']
    data.pop('project_id')
    return ProjectLocationsEndpoint(token, project_id).post(data)


def get_project_locations(token, project_id):
    return ProjectLocationsEndpoint(token, project_id).get()


def get_location(token, location_id):
    return APICallLocation(token, location_id).get()


def update_location(token, location_id, data):
    return APICallLocation(token, location_id).put(data)


def delete_location(token, location_id):
    return APICallLocation(token, location_id).delete()
