import tera_etl.quality_control as qc


data_test = {
    "UserProfileSchema": {
        "UserId": "090349324324",
        "HomePhone": "0369841490",
        "WorkPhone": None,
        "AddrHouseNo": "",
        "AddrStreetName": "",
        "AddrWard": "15 NGÕ 341, Phường Xuân Phương",
        "AddrDistrict": "Quận Nam Từ Liêm",
        "AddrProvince": "Thành phố Hà Nội",
        "AddrCountry": "Việt Nam",
        "Firstname": "NGUYỄN THỊ BÍCH ",
        "Lastname": "HIỀN",
        "Gender": "Female",
        "RegisterDate": "2022-01-01T00:00:00.00Z",
        "DataSource": "VTVHyundai",
        "MaritalStatus": "Single"
    }
}


def test_quality_control_validate_format_redundant_columns():
    schema_name = 'UserProfileSchema'
    new_case_data = data_test['UserProfileSchema'].copy()
    new_case_data['RedundantKey'] = 'TEST'
    qc_result = qc.classify_data(data_chunk=new_case_data, schema_name=schema_name)
    assert qc_result['qc_type'] == qc.QualityControlResult.REJECTED
    assert qc_result['errors'] == {'RedundantKey': ['Unknown field.']}


def test_quality_control_validate_format_missing_columns():
    schema_name = 'UserProfileSchema'
    new_case_data = data_test['UserProfileSchema'].copy()
    del new_case_data['UserId']
    qc_result = qc.classify_data(data_chunk=new_case_data, schema_name=schema_name)
    assert qc_result['qc_type'] == qc.QualityControlResult.REJECTED
    assert qc_result['errors'] == {'UserId': ['Missing data for required field.']}


def test_quality_control_validate_gender():
    schema_name = 'UserProfileSchema'
    new_case_data = data_test['UserProfileSchema'].copy()
    new_case_data['Gender'] = 'TEST'
    qc_result = qc.classify_data(data_chunk=new_case_data, schema_name=schema_name)
    assert qc_result['qc_type'] == qc.QualityControlResult.REJECTED
    assert qc_result['errors'] == {'Gender': ['Must be one of: Male, Female, Other.']}


def test_quality_control_validate_marital_status():
    schema_name = 'UserProfileSchema'
    new_case_data = data_test['UserProfileSchema'].copy()
    new_case_data['MaritalStatus'] = 'TEST'
    qc_result = qc.classify_data(data_chunk=new_case_data, schema_name=schema_name)
    assert qc_result['qc_type'] == qc.QualityControlResult.REJECTED
    assert qc_result['errors'] == {'MaritalStatus': ['Must be one of: Single, Married.']}


def test_quality_control_validate_datetime_format():
    schema_name = 'UserProfileSchema'
    new_case_data = data_test['UserProfileSchema'].copy()
    new_case_data['RegisterDate'] = 'TEST'
    qc_result = qc.classify_data(data_chunk=new_case_data, schema_name=schema_name)
    assert qc_result['qc_type'] == qc.QualityControlResult.REJECTED
    assert qc_result['errors'] == {'RegisterDate': ['Not a valid datetime.']}


def test_quality_control_validate_null():
    schema_name = 'UserProfileSchema'
    new_case_data = data_test['UserProfileSchema'].copy()
    new_case_data['UserId'] = None
    new_case_data['Firstname'] = None
    qc_result = qc.classify_data(data_chunk=new_case_data, schema_name=schema_name)
    assert qc_result['qc_type'] == qc.QualityControlResult.REJECTED
    assert qc_result['errors'] == {'UserId': ['Field may not be null.'], 'Firstname': ['Field may not be null.']}


def test_perform_quality_control():
    qc_result = qc.classify_data(data_chunk=data_test['UserProfileSchema'], schema_name='UserProfileSchema')
    assert qc_result['qc_type'] == qc.QualityControlResult.ACCEPTED
