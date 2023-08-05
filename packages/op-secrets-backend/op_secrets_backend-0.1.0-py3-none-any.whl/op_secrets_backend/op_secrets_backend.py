# this is a library used by dag users
from airflow.secrets import BaseSecretsBackend

import requests
import os
import json
import logging

log = logging.getLogger(__name__)


class OpSecretsBackend(BaseSecretsBackend):
    def get_connection(self, conn_id: str): # conn_id here is OP connection name
        from airflow.models.taskinstance import _CURRENT_CONTEXT
        from airflow.configuration import ensure_secrets_loaded
        from airflow.exceptions import AirflowNotFoundException
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
            for secrets_backend in ensure_secrets_loaded():
                type_check_result = isinstance(secrets_backend, OpSecretsBackend)
                if type_check_result is False:
                    try:
                        conn = secrets_backend.get_connection(conn_id=result[1])
                        if conn:
                            return conn
                    except Exception:
                        log.exception(
                            "Unable to retrieve connection from secrets backend (%s). "
                            "Checking subsequent secrets backend.",
                            type(secrets_backend).__name__,
                        )

            raise AirflowNotFoundException(f"The conn_id `{result[1]}` isn't defined")
        else:
            raise Exception(result[1])
    