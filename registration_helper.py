import json
import os

last_device_json_file_path = "last-device-requsted.json"

def is_reg_info_json_created():
    if(os.path.exists(last_device_json_file_path)):
        try:
            reg_inf = read_reg_info_json()
            if(reg_inf["serial_number"]):
                return True
        except:
            return False
    
    return False

def create_reg_info_json(registration_info):
    with open(last_device_json_file_path, "w") as outfile:
        outfile.write(json.dumps(registration_info.__dict__))

def read_reg_info_json():
    with open(last_device_json_file_path, "r") as json_file:
        return json.loads(json_file.read())

def remove_reg_info_json(serial_number):
    if(is_reg_info_json_created()):
        reg_info = read_reg_info_json()
        if(serial_number == reg_info['serial_number']):
            os.remove(last_device_json_file_path)