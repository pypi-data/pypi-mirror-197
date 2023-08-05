# this is a library used by dag users
from airflow.secrets import BaseSecretsBackend
import requests
import os
import json


class OpSecretsBackend(BaseSecretsBackend):
    def get_connection(self, conn_id: str): # conn_id here is OP connection name
        from airflow.models.taskinstance import _CURRENT_CONTEXT
        if _CURRENT_CONTEXT is None or len(_CURRENT_CONTEXT) == 0:
            raise Exception("failed to get _CURRENT_CONTEXT") 
        run_id = _CURRENT_CONTEXT[0]["dag_run"].run_id
        dag_id = _CURRENT_CONTEXT[0]["dag_run"].dag_id
        id = _CURRENT_CONTEXT[0]["dag_run"].id
        AC_URL = os.getenv('AC_URL')
        param_values={'run_id':run_id, 'dag_id':dag_id, 'id':id, 'user_connection_name':conn_id}
        url=AC_URL+"/airflow-connection-id"
        response = requests.get(url, params = param_values)
        if response is None or response.status_code != 200:
            raise Exception("Cannot connect with AC") 
        result = json.loads(response.text)
        if result[0] == 200:
            return super().get_connection(result[1])
        else:
            raise Exception(result[1])
    