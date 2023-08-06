from tera_etl.utils.consolidate_utils import merge_user_profile_data
import copy


base_data = [
    {
        'UserId': 'base_data',
        'HomePhone': 'base_data',
        'WorkPhone': 'base_data',
        'AddrHouseNo': 'base_data',
        'AddrStreetName': 'base_data',
        'AddrWard': 'base_data',
        'AddrDistrict': 'base_data',
        'AddrProvince': 'base_data',
        'AddrCountry': 'base_data',
        'Firstname': 'base_data',
        'Lastname': 'base_data',
        'Gender': 'base_data',
        'RegisterDate': 'base_data',
        'DataSource': 'base_data',
        'MaritalStatus': 'base_data'
    }
]


ingest_data = [
    {
        'UserId': 'ingest_data',
        'HomePhone': 'ingest_data',
        'WorkPhone': 'ingest_data',
        'AddrHouseNo': 'ingest_data',
        'AddrStreetName': 'ingest_data',
        'AddrWard': 'ingest_data',
        'AddrDistrict': 'ingest_data',
        'AddrProvince': 'ingest_data',
        'AddrCountry': 'ingest_data',
        'Firstname': 'ingest_data',
        'Lastname': 'ingest_data',
        'Gender': 'ingest_data',
        'RegisterDate': 'ingest_data',
        'DataSource': 'ingest_data',
        'MaritalStatus': 'ingest_data'
    },
]


def test_merge_user_profile_data():
    # CASE no duplicate phone number
    ingest_data_new_case = copy.deepcopy(ingest_data)
    base_data_new_case = copy.deepcopy(base_data)
    ingest_data_new_case[0]['HomePhone'] = 'test'
    res = merge_user_profile_data(
        ingest_data_new_case, base_data_new_case)
    assert len(res) == len(base_data_new_case) + 1
    assert res[-1] == ingest_data_new_case[0]

    # CASE duplicate phone number
    # Datasource same priority
    # Updating data from new ingest data
    ingest_data_new_case = copy.deepcopy(ingest_data)
    base_data_new_case = copy.deepcopy(base_data)
    ingest_data_new_case[0]['HomePhone'] = base_data_new_case[0]['HomePhone']
    ingest_data_new_case[0]['DataSource'] = 'VTVcab CRM'
    base_data_new_case[0]['DataSource'] = 'VTVcab CRM'
    res = merge_user_profile_data(ingest_data_new_case, base_data_new_case)
    assert len(res) == len(base_data_new_case)
    assert res[0]['UserId'] == ingest_data_new_case[0]['UserId']
    assert res[0]['WorkPhone'] == ingest_data_new_case[0]['WorkPhone']
    assert res[0]['Firstname'] == ingest_data_new_case[0]['Firstname']

    # Datasource difference priority ("VTVcab CRM" higher priority than VTVHyundai)
    # Updating data from new ingest data
    ingest_data_new_case = copy.deepcopy(ingest_data)
    base_data_new_case = copy.deepcopy(base_data)
    ingest_data_new_case[0]['HomePhone'] = base_data_new_case[0]['HomePhone']
    ingest_data_new_case[0]['DataSource'] = 'VTVcab CRM'
    base_data_new_case[0]['DataSource'] = 'VTVHyundai'
    res = merge_user_profile_data(ingest_data_new_case, base_data_new_case)
    assert len(res) == len(base_data_new_case)
    assert res[0]['UserId'] == ingest_data_new_case[0]['UserId']
    assert res[0]['WorkPhone'] == ingest_data_new_case[0]['WorkPhone']
    assert res[0]['Firstname'] == ingest_data_new_case[0]['Firstname']

    # Keeping old data
    ingest_data_new_case = copy.deepcopy(ingest_data)
    base_data_new_case = copy.deepcopy(base_data)
    ingest_data_new_case[0]['HomePhone'] = base_data_new_case[0]['HomePhone']
    ingest_data_new_case[0]['DataSource'] = 'VTVHyundai'
    base_data_new_case[0]['DataSource'] = 'VTVcab CRM'
    res = merge_user_profile_data(
        ingest_data_new_case, base_data_new_case)
    assert len(res) == len(base_data_new_case)
    assert res[0]['UserId'] == base_data_new_case[0]['UserId']
    assert res[0]['WorkPhone'] == base_data_new_case[0]['WorkPhone']
    assert res[0]['Firstname'] == base_data_new_case[0]['Firstname']

    # Updating the fields that are missing from the new ingest data
    ingest_data_new_case = copy.deepcopy(ingest_data)
    base_data_new_case = copy.deepcopy(base_data)
    ingest_data_new_case[0]['HomePhone'] = base_data_new_case[0]['HomePhone']
    del base_data_new_case[0]['Firstname']
    del base_data_new_case[0]['Lastname']
    ingest_data_new_case[0]['DataSource'] = 'VTVHyundai'
    base_data_new_case[0]['DataSource'] = 'VTVcab CRM'
    res = merge_user_profile_data(ingest_data_new_case, base_data_new_case)
    assert len(res) == len(base_data_new_case)
    assert 'Firstname' in res[0]
    assert 'Lastname' in res[0]
    assert res[0]['Firstname'] == ingest_data_new_case[0]['Firstname']
    assert res[0]['Lastname'] == ingest_data_new_case[0]['Lastname']

    # Not update null or empty fields from the new ingest data
    ingest_data_new_case = copy.deepcopy(ingest_data)
    base_data_new_case = copy.deepcopy(base_data)
    ingest_data_new_case[0]['HomePhone'] = base_data_new_case[0]['HomePhone']
    ingest_data_new_case[0]['Firstname'] = None
    ingest_data_new_case[0]['Lastname'] = ''
    ingest_data_new_case[0]['DataSource'] = 'VTVcab CRM'
    base_data_new_case[0]['DataSource'] = 'VTVHyundai'
    res = merge_user_profile_data(ingest_data_new_case, base_data_new_case)
    assert len(res) == len(base_data_new_case)
    assert res[0]['Firstname'] == base_data_new_case[0]['Firstname']
    assert res[0]['Lastname'] == base_data_new_case[0]['Lastname']

    # CASE duplicate user id
    # Datasource same priority
    # Updating data from new ingest data
    ingest_data_new_case = copy.deepcopy(ingest_data)
    base_data_new_case = copy.deepcopy(base_data)
    ingest_data_new_case[0]['UserId'] = base_data_new_case[0]['UserId']
    ingest_data_new_case[0]['DataSource'] = 'VTVcab CRM'
    base_data_new_case[0]['DataSource'] = 'VTVcab CRM'
    res = merge_user_profile_data(ingest_data_new_case, base_data_new_case)
    assert len(res) == len(base_data_new_case)
    assert res[0]['UserId'] == ingest_data_new_case[0]['UserId']
    assert res[0]['WorkPhone'] == ingest_data_new_case[0]['WorkPhone']
    assert res[0]['Firstname'] == ingest_data_new_case[0]['Firstname']

    # Datasource difference priority ("VTVcab CRM" higher priority than VTVHyundai)
    # Updating data from new ingest data
    ingest_data_new_case = copy.deepcopy(ingest_data)
    base_data_new_case = copy.deepcopy(base_data)
    ingest_data_new_case[0]['UserId'] = base_data_new_case[0]['UserId']
    ingest_data_new_case[0]['DataSource'] = 'VTVcab CRM'
    base_data_new_case[0]['DataSource'] = 'VTVHyundai'
    res = merge_user_profile_data(
        ingest_data_new_case, base_data_new_case)
    assert len(res) == len(base_data_new_case)
    assert res[0]['UserId'] == ingest_data_new_case[0]['UserId']
    assert res[0]['WorkPhone'] == ingest_data_new_case[0]['WorkPhone']
    assert res[0]['Firstname'] == ingest_data_new_case[0]['Firstname']

    # Keeping old data
    ingest_data_new_case = copy.deepcopy(ingest_data)
    base_data_new_case = copy.deepcopy(base_data)
    ingest_data_new_case[0]['UserId'] = base_data_new_case[0]['UserId']
    ingest_data_new_case[0]['DataSource'] = 'VTVHyundai'
    base_data_new_case[0]['DataSource'] = 'VTVcab CRM'
    res = merge_user_profile_data(ingest_data_new_case, base_data_new_case)
    assert len(res) == len(base_data_new_case)
    assert res[0]['UserId'] == base_data_new_case[0]['UserId']
    assert res[0]['WorkPhone'] == base_data_new_case[0]['WorkPhone']
    assert res[0]['Firstname'] == base_data_new_case[0]['Firstname']

    # Updating the fields that are missing from the new ingest data
    ingest_data_new_case = copy.deepcopy(ingest_data)
    base_data_new_case = copy.deepcopy(base_data)
    ingest_data_new_case[0]['UserId'] = base_data_new_case[0]['UserId']
    del base_data_new_case[0]['Firstname']
    del base_data_new_case[0]['Lastname']
    ingest_data_new_case[0]['DataSource'] = 'VTVHyundai'
    base_data_new_case[0]['DataSource'] = 'VTVcab CRM'
    res = merge_user_profile_data(ingest_data_new_case, base_data_new_case)
    assert len(res) == len(base_data_new_case)
    assert 'Firstname' in res[0]
    assert 'Lastname' in res[0]
    assert res[0]['Firstname'] == ingest_data_new_case[0]['Firstname']
    assert res[0]['Lastname'] == ingest_data_new_case[0]['Lastname']

    # Not update null or empty fields from the new ingest data
    ingest_data_new_case = copy.deepcopy(ingest_data)
    base_data_new_case = copy.deepcopy(base_data)
    ingest_data_new_case[0]['UserId'] = base_data_new_case[0]['UserId']
    ingest_data_new_case[0]['Firstname'] = None
    ingest_data_new_case[0]['Lastname'] = ''
    ingest_data_new_case[0]['DataSource'] = 'VTVcab CRM'
    base_data_new_case[0]['DataSource'] = 'VTVHyundai'
    res = merge_user_profile_data(ingest_data_new_case, base_data_new_case)
    assert len(res) == len(base_data_new_case)
    assert res[0]['Firstname'] == base_data_new_case[0]['Firstname']
    assert res[0]['Lastname'] == base_data_new_case[0]['Lastname']
