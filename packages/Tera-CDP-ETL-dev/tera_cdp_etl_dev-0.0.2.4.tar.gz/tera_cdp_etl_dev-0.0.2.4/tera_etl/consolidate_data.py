from tera_etl.utils.consolidate_utils import merge_user_profile_data


def consolidate_data(ingest_data, base_data, schema_name) -> dict:
    return __consolidate(ingest_data, base_data, schema_name)


def __consolidate(ingest_data, base_data, schema_name):
    result = []
    if schema_name == 'UserProfileSchema':
        result = merge_user_profile_data(ingest_data, base_data)
    if schema_name == "UserWatchVideoSchema":
        pass
    return result
