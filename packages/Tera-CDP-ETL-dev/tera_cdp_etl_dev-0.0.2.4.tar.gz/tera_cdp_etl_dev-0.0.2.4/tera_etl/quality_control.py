from enum import Enum
from tera_etl.validations import schemas

schema_dict = {
    "UserProfileSchema": schemas.UserProfileSchema(),
    "UserWatchVideoSchema": schemas.UserWatchVideoSchema(),
}


class QualityControlResult(Enum):
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'


def classify_data(data_chunk, schema_name, **kwargs) -> dict:
    is_accepted = __is_accepted(data_chunk, schema_name)
    return {
        "qc_type": QualityControlResult.ACCEPTED if is_accepted["status"] else QualityControlResult.REJECTED,
        "errors": is_accepted["errors"]
    }


def __is_accepted(chunk, schema_name):
    return __has_valid_schema(chunk, schema_name)


def __has_valid_schema(data, schema_name):
    errors = schema_dict[schema_name].validate(data)
    return {
        "status": True if not errors else False,
        "errors": errors,
    }
