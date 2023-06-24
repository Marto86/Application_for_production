import string
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QPlainTextEdit,
    QVBoxLayout,
    QWidget,
)
from subprocess import PIPE, Popen
from PyQt5.QtCore import QProcess
import tb_flash_board
import sys
import argparse
from ast import For
from cmd import PROMPT
import cmd
from typing import Counter
from click import prompt
import time
import serial
import json
import csv
from csv import writer
import subprocess
import os
from PIL import Image
from sympy import false, true
from zebra import Zebra
import requests
import shutil
import tempfile
from cloud_ingeli_registerer import *
from PyQt5 import QtCore
import registration_helper as rh

ingeliConfig = json.load(open("configs/ingeliConfig.json"))
registerer = CloudIngeliRegisterer(ingeliConfig["provisioningApiUrl"],ingeliConfig["token"]) # class to do request

# ZPL commands to be sent to your Printer
def print_4G_label(gw_serial_number,imei,simSN):


    label = f"""
^CI27
^PA0,1,1,0
^XZ
^XA
^FWB
^BY1,3,1^FO20,110^BCN,60,N,N,N,A^FD{gw_serial_number}^FS
^FO0,110^GB400,1,1^FS
^FWN
^CFB,16 
^FO5,20^FDGateway^FS ^FO32,50^FDIMEI^FS ^FO23,80^FDICCID^FS
^CFQ,16 ^FO80,13^FD{gw_serial_number}^FS
^FO80,43^FD{imei}^FS ^FO80,73^FD{simSN}^FS ^FO325,20^GFA,590,590,10,,:Q0FC,Q0FF8,Q0IF,Q0IFC,R03FE,S07F8,S01FC,T07E,Q07C03F,Q07F01F8,Q07FC0FC,Q07FF07C,R07F83E,R01FC1F,S07E0F,S03E0F8,S01F078,Q0700F878,Q07C0783C,Q07E07C3C,Q07F03C3C,Q01F83C3C,R0F83C1E,R0781E1E,R03C1E1E,O07803C1E1E,I07EI07FF8,I0FFI0IFC,001FF003IFE,001FF007IFE,003FF007IFC,007FF00FF01C,007FF01FE,00FBF01FC,00FBF01F8,01F3F03F8,03F3F03F8,03E3F03F,07E3F03F03FF,0FC3F03F03FF,0F83F03F03FF,1F83F03F03FF,1JFE3F81FF,1JFE3F801F,1JFE1F801F,1JFE1FC01F,1JFE1FE01F,I03F00FF03F,I03F007JF,:I03F003JF,I03FI0IFE,I03FI03FF8,O01,,::^FS
^XZ
^FX Third section with bar code.
^BY5,2,270
^FO100,550^BC^FD12345678^FS
^FX Fourth section (the two boxes on the bottom).
^FO50,900^GB700,250,3^FS
^FO400,900^GB3,250,3^FS
^CF0,40
^FO100,960^FDCtr. X34B-1^FS
^FO100,1010^FDREF1 F00B47^FS
^FO100,1060^FDREF2 BL4H8^FS
^CF0,190
^FO470,955^FDCA^FS
^XZ
"""
    z = Zebra()
    print("Printer queues found:", z.getqueues())
    # z.getqueues
    z.setqueue("Zebra_Technologies_ZTC_ZT220-200dpi_ZPL")
    z.output(label)
    url = "http://api.labelary.com/v1/printers/8dpmm/labels/2.1x0.9/0/"
    files = {"file": label}
    response = requests.post(url, files=files, stream=True)
    if response.status_code == 200:
        response.raw.decode_content = True
        with open("label.PNG", "wb") as out_file:  # change file name for PNG images
            shutil.copyfileobj(response.raw, out_file)
    else:
        print("Error: " + response.text)


def print_label(gw_serial_number):


    label = f"""
^CI27
^PA0,1,1,0
^XZ
^XA
^FWB
^BY1,3,1^FO20,110^BCN,60,N,N,N,A^FD{gw_serial_number}^FS
^FO0,110^GB400,1,1^FS
^FWN
^CFB,16 ^FO5,20^FDGateway^FS
^CFQ,16 ^FO80,13^FD{gw_serial_number}^FS 
^XZ
"""
    z = Zebra()
    print("Printer queues found:", z.getqueues())
    #z.getqueues
    z.setqueue("Zebra_Technologies_ZTC_ZT220-200dpi_ZPL")
    z.output(label)
    url = "http://api.labelary.com/v1/printers/8dpmm/labels/2.1x0.9/0/"
    files = {"file": label}
    response = requests.post(url, files=files, stream=True)
    if response.status_code == 200:
        response.raw.decode_content = True
        with open("label.PNG", "wb") as out_file:  # change file name for PNG images
            shutil.copyfileobj(response.raw, out_file)
    else:
        print("Error: " + response.text)

def flash_firmware(on_command_output_cb):
    gateway_config = json.load(open("configs/gatewayConfig.json"))
    subprocess.run(f"export IDF_PATH={gateway_config['idfPath']}", shell=True)
    cmd_export_Idf_Paths = f". {gateway_config['idfPath']}/export.sh"
    cmd_create_Nvs_Bin =  f"{gateway_config['pythonPath']} {gateway_config['idfPath']}/components/nvs_flash/nvs_partition_generator/nvs_partition_gen.py generate provisioning/provisioning.csv provisioning/provisioning.bin 0x4000"
    firmware_bins_folder = f"firmware/{gateway_config['firmwareVersion']}"
    provisioning_bin_path = "provisioning/provisioning.bin"
    cmd_flash_Fw = f"{gateway_config['pythonPath']} {gateway_config['idfPath']}/components/esptool_py/esptool/esptool.py -p {gateway_config['usb']} -b 460800 --before default_reset --after hard_reset --chip esp32s3 write_flash --flash_mode dio --flash_freq 80m --flash_size detect 0x10000 {firmware_bins_folder}/LTEgateway.bin 0x0 {firmware_bins_folder}/bootloader.bin 0x8000 {firmware_bins_folder}/partition-table.bin 0xd000 {firmware_bins_folder}/ota_data_initial.bin 0xc14000 {provisioning_bin_path}"
    
    export_Idf_Paths = subprocess.run(
        cmd_export_Idf_Paths,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    on_command_output_cb(export_Idf_Paths.stdout)

    create_Nvs_Bin = subprocess.run(
        cmd_create_Nvs_Bin,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    on_command_output_cb(create_Nvs_Bin.stdout)

    flash_Fw = subprocess.run(
        cmd_flash_Fw,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    on_command_output_cb(flash_Fw.stdout)

    if flash_Fw.returncode == 0:
        return True
    else:
        return False

def flash_procedure(firmware_version, hardware_version, on_command_executed_cb):
    is_registered = None
    registration_info = None
    if(rh.is_reg_info_json_created()):
        is_registered = True
        registration_infos_json = rh.read_reg_info_json()
        registration_info = RegistrationInfos(registration_infos_json['uuid'], registration_infos_json['serial_number'], registration_infos_json['sector'], registration_infos_json['login'], registration_infos_json['password'])
    else: 
        is_registered, registration_info = registerer.try_register(firmware_version, hardware_version) #post request to ask for credentials
        rh.create_reg_info_json(registration_info)

    if not is_registered:
        on_command_executed_cb("Could not register device! Possibly can not connect to the provisioning API or something else!")
        return False
    
    data = open(
        "provisioning/provisioning_template.csv",
        "r",
    )
    data = "".join([i for i in data])
    data = data.replace("{serial}", registration_info.serial_number)
    data = data.replace("{uuid}", str(registration_info.uuid))
    data = data.replace("{sector}", str(registration_info.sector))
    data = data.replace("{mqtt_cl_id}", registration_info.login)
    data = data.replace("{mqtt_cl_user}", registration_info.login)
    data = data.replace("{mqtt_pass}", registration_info.password)

    out_csv = open(
        "provisioning/provisioning.csv",
        "w",
    )
    out_csv.writelines(data)
    out_csv.close()

    return flash_firmware(on_command_executed_cb)

def get_last_flashed_serial_number():
    with open("provisioning/provisioning.csv", newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if(row['key'] == 'serial'):
                return row['value']




def test_cb(text):
    print(f"log :{text}")
