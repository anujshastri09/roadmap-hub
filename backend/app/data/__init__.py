from app.data.python_developer import PYTHON_DEVELOPER
from app.data.mern_stack import MERN_STACK
from app.data.java_developer import JAVA_DEVELOPER
from app.data.aws_cloud import AWS_CLOUD
from app.data.system_design import SYSTEM_DESIGN

ALL_FIELDS = [
    PYTHON_DEVELOPER,
    MERN_STACK,
    JAVA_DEVELOPER,
    AWS_CLOUD,
    SYSTEM_DESIGN,
]

FIELDS_BY_ID = {field["id"]: field for field in ALL_FIELDS}
