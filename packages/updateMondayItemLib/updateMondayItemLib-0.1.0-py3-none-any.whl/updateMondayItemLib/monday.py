import requests
import json

def update_testcase_status(apiKey,apiUrl,board_id,item_id, **columnValuesDict):  
    request_headers = {"Authorization" : apiKey}
    for key in columnValuesDict:
        columns_Dict = {
        key: columnValuesDict[key],
        }  
        vars = {
       'item_id' : int(item_id),
        'board_id' : int(board_id),
         'columnVals' : json.dumps(columns_Dict)
         } 
        query =  'mutation ( $board_id: Int!, $item_id: Int!,  $columnVals: JSON!) {change_multiple_column_values (board_id: $board_id, item_id: $item_id, column_values: $columnVals) {id}}'
        data = {'query' : query,'variables' : vars}
        requests.post(url=apiUrl, json=data, headers=request_headers)


