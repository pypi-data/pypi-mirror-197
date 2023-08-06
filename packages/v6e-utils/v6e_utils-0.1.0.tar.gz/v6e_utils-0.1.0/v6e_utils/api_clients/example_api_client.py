#  Copyright (c) 2023. ISTMO Center S.A.  All Rights Reserved
#
from .api_client import V6eApiClient


class ExampleApiClient(V6eApiClient):

    def get_bank_list(self, params):
        endpoint = "banks"
        return self.get(endpoint, params)

    def get_department_list(self, params):
        endpoint = "departments"
        return self.get(endpoint, params)
