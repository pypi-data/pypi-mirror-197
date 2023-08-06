import os
import json
import warnings
from dotenv import load_dotenv


if os.getenv('ENV_FILE', None):
    load_dotenv(os.getenv('ENV_FILE'))

UNSAFE_SECRET_ = "ab8374b5e38473c4a05c9f95c06cfc4b"


class Config:
    schema_name = os.getenv('SCHEMA_NAME', 'main')
    database_url = os.getenv(
            'SQLALCHEMY_DATABASE_URI',
            'sqlite:///metastore.db'
            )
    superset_base_url = os.getenv('SUPERSET_BASE_URL')
    superset_password = os.getenv('SUPERSET_ADMIN_PASSWORD')
    superset_username = os.getenv('SUPERSET_USERNAME')
    airflow_task_name = os.getenv(
            'AIRFLOW_TASK_NAME',
            'superset_cleaning_task'
            )
    airflow_dag_name = os.getenv(
            'AIRFLOW_DAG_NAME',
            'superset_cleaning_dag'
            )
    airflow_run_id = os.getenv(
            'AIRFLOW_TASK_RUN_ID',
            'superset_cleaning_task_run_id'
            )
    log_level = os.getenv('LOG_LEVEL', 'DEBUG')
    color_palette_size = os.getenv('COLOR_PALLET_SIZE', 50)
    airflow_base_url = os.getenv(
            'AIRFLOW_BASE_URL',
            'http://localhost:8080'
            )
    track_db_modifications = os.getenv(
            'SQLALCHEMY_TRACK_MODIFICATIONS',
            False)

    secret_key = os.getenv('SECRET_KEY', UNSAFE_SECRET_)
    if secret_key == UNSAFE_SECRET_:
        warnings.warn("You are using an insecure secret "
                      "key!!! It is essential to change "
                      "this in production")
    keycloak_url = os.getenv('KEYCLOAK_URL')
    keycloak_realm = os.getenv('KEYCLOAK_REALM')
    keycloak_client_secret = os.getenv('KEYCLOAK_CLIENT_SECRET')
    keycloak_client_id = os.getenv('KEYCLOAK_CLIENT_ID')
    host = os.getenv('HOST', 'http://localhost:5000')
    oauth = (os.getenv('OAUTH', 'False').lower() == 'true')


def sqlalchemy_track_modif(
        client_secret_path=os.getenv(
                'CLIENT_SECRET_FILEPATH',
                'client_secrets.json')
        ):
    conf = {
            "web": {
                    "issuer": f"{Config.keycloak_url}/auth"
                              f"/realms/{Config.keycloak_realm}",
                    "auth_uri": f"{Config.keycloak_url}/auth"
                                f"/realms/{Config.keycloak_realm}/protocol"
                                f"/openid-connect/auth",
                    "token_uri": f"{Config.keycloak_url}/auth"
                                 f"/realms/{Config.keycloak_realm}/protocol"
                                 f"/openid-connect/token",
                    "token_introspection_uri": f"{Config.keycloak_url}/auth"
                                               f"/realms/"
                                               f"{Config.keycloak_realm}"
                                               f"/protocol/openid"
                                               f"-connect/token/introspect",
                    "client_id": Config.keycloak_client_id,
                    "client_secret": Config.keycloak_client_secret,
                    }
            }
    with open('client_secrets.json', 'w') as f:
        f.write(json.dumps(conf))
    return client_secret_path


class ConfigExtenderUI:
    SQLALCHEMY_DATABASE_URI = Config.database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = Config.track_db_modifications
    SECRET_KEY = Config.secret_key
    OIDC_CLIENT_SECRETS = sqlalchemy_track_modif()
    OIDC_ID_TOKEN_COOKIE_SECURE = False
    OIDC_REQUIRE_VERIFIED_EMAIL = False
    OIDC_COOKIE_SECURE = False
    OIDC_USER_INFO_ENABLED = True
    OIDC_OPENID_REALM = Config.keycloak_realm
    OIDC_SCOPES = ['openid', 'email', 'profile']
    OIDC_TOKEN_TYPE_HINT = 'access_token'
    OIDC_INTROSPECTION_AUTH_METHOD = 'client_secret_post'
