import os

TAG = os.getenv('TAG', '1.0.0')
__version__ = os.getenv('CI_COMMIT_TAG', TAG)

__superset_version__ = '2.0'
