import registration_helper as rh
import json

is_successful = True
if(not rh.is_reg_info_json_created()):
    rh.create_reg_info_json(json.loads('{"serial_number": "123"}'))

if(not rh.is_reg_info_json_created()):
    print("Error create_reg_info_json not working")
    is_successful = False
else:
    rh.remove_reg_info_json("123")
    if(rh.is_reg_info_json_created()):
        print("Error remove_reg_info_json not working")
        is_successful = False

if(is_successful):
    print("Test successful!!!")
else:
    print("Test failed!!!")
