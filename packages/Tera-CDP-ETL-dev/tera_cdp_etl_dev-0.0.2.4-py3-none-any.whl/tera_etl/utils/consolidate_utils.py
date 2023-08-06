import copy

# Define a dictionary with priorities for merging data based on the DataSource field
DATA_PROVIDER_PRIORITIES = {
    'vtvcabcrm': 1,
    'vtvhyundai': 2,
}

# Define a dictionary with priorities for merging data based on certain key fields
CONSOLIDATE_KEY_PRIORITIES = {
    'HomePhone': 1,
    'UserId': 2,
}

# Define the main function for merging user profile data
def merge_user_profile_data(ingest_data, base_data):
    # Make a deep copy of the base data list
    result = copy.deepcopy(base_data)
    
    # Create a dictionary to keep track of the index positions of items in the result list
    pre_data = {}
    for k in CONSOLIDATE_KEY_PRIORITIES.keys():
        pre_data[k]= {}
        
    # Loop through each item in the result list and create an entry in the pre_data dictionary
    # for each consolidate key field
    for i, item in enumerate(result):
        for k in CONSOLIDATE_KEY_PRIORITIES.keys():
            pre_data[k][item[k]] = i
            
    # Loop through each item in the ingest_data list
    for item in ingest_data:
        # Call a helper function to determine which consolidate key field to use
        consolidated_key = __get_consolidated_key(pre_data, item)
        
        # If the consolidate key field is not found in the pre_data dictionary,
        # add the item to the end of the result list and update the pre_data dictionary
        if not consolidated_key:
            result.append(item)
            for k in CONSOLIDATE_KEY_PRIORITIES.keys():
                pre_data[k][item[k]] = len(result)
                
        # If the consolidate key field is found in the pre_data dictionary,
        # call another helper function to determine the index position of the item in the result list
        else:
            index_item = __get_index_item_by_type(pre_data, item, consolidated_key)
            
            # Compare the DataSource fields of the two items to determine priority
            if DATA_PROVIDER_PRIORITIES[(item['DataSource'].lower()).replace(' ', "")] <= DATA_PROVIDER_PRIORITIES[(result[index_item]['DataSource'].lower()).replace(' ', "")]:
                # If the ingest_data item has higher priority, update the fields of the corresponding item in the result list
                for key, value in item.items():
                    if value:
                        result[index_item][key] = value
            else:
                # If the result item has higher priority, do not update any fields, only add missing fields 
                for key, value in item.items():
                    if key not in result[index_item] and value:
                        result[index_item][key] = value
                        
    # Return the merged set of data
    return result

# Define a helper function to determine which consolidate key field to use
def __get_consolidated_key(pre_data, item):
    consolidated_key = ''
    for k in CONSOLIDATE_KEY_PRIORITIES.keys():
        if item[k] in pre_data[k]:
            consolidated_key = k
            break
    return consolidated_key

# Define a helper function to determine the index position of the item in the result list
def __get_index_item_by_type(pre_data, item, consolidated_key):
    index_item_by_consolidated_key = {
        'HomePhone': pre_data[consolidated_key][item[consolidated_key]],
        'UserId': pre_data[consolidated_key][item[consolidated_key]],
    }
    return index_item_by_consolidated_key[consolidated_key]
