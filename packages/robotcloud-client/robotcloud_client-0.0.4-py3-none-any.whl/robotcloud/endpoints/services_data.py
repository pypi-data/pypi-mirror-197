from abc import ABCMeta

from robotcloud.api import APIEndPointAuthenticated


class APICallServiceInstance(APIEndPointAuthenticated, metaclass=ABCMeta):
    def __init__(self, token: str, project_id: str, service_type: str, instance_id: str = None):
        self.project_id = project_id
        self.service_type = service_type
        self.instance_id = instance_id
        super().__init__(token)


class APICallServiceInstanceData(APICallServiceInstance):
    """
        Implement GET
    """

    def get_endpoint(self):
        if self.instance_id is None:
            return f'projects/{self.project_id}/services/{self.service_type}/data'
        else:
            return f'projects/{self.project_id}/services/{self.service_type}/instances/{self.instance_id}/data'


class APICallServiceInstanceConfig(APICallServiceInstance):
    """
        Implement GET, PUT methods
    """

    def get_endpoint(self):
        if self.instance_id is None:
            return f'projects/{self.project_id}/services/{self.service_type}/configuration'
        else:
            return f'projects/{self.project_id}/services/{self.service_type}/instances/{self.instance_id}/configuration'


class APICallServiceInstanceAlert(APICallServiceInstance):
    """
        Implement GET
    """

    def get_endpoint(self):
        if self.instance_id is None:
            return f'projects/{self.project_id}/services/{self.service_type}/alert'
        else:
            return f'projects/{self.project_id}/services/{self.service_type}/instances/{self.instance_id}/alert'


def get_service_instance_data(token, project_id, service_type, instance_id=None) -> dict:
    """
    If instance_id is None then return data from all project service_type instances
    otherwise, only return the data from the specified instance.

    :param token:
    :param project_id:
    :param service_type:
    :param instance_id:
    :raises:
    :return:
    """
    api_response = APICallServiceInstanceData(token, project_id, service_type, instance_id).get()
    if type(api_response) is dict:
        return api_response  # Single data

    response = {}
    for data in api_response:
        response[data['instance']] = data

    return response


def get_service_instance_config(token, project_id, service_type, instance_id):
    """
    If instance_id is None then return data from all project service_type instances
    otherwise, only return the data from the specified instance.

    :param token:
    :param project_id:
    :param service_type:
    :param instance_id:
    :return:
    """
    return APICallServiceInstanceConfig(token, project_id, service_type, instance_id).get()


def update_service_instance_config(token, project_id, service_type, instance_id, data):
    """
    Update the specified service instance configuration.

    :param token:
    :param project_id:
    :param service_type:
    :param instance_id:
    :param data: Data to update
    :return:
    """
    return APICallServiceInstanceConfig(token, project_id, service_type, instance_id).put(data)


def get_service_instance_alert(token, project_id, service_type, instance_id=None) -> dict:
    """
    If instance_id is None then return data from all project service_type instances
    otherwise, only return the data from the specified instance.

    :param token:
    :param project_id:
    :param service_type:
    :param instance_id:
    :return:
    """
    api_response = APICallServiceInstanceAlert(token, project_id, service_type, instance_id).get()
    if type(api_response) is dict:
        return api_response  # Single data

    response = {}
    for data in api_response:
        response[data['instance']] = data

    return response
