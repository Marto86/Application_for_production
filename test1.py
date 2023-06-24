from sympy import true
import tb_flash_board as fb
import sys
import subprocess as sb
import gateway_identifier
import json
from cloud_ingeli_registerer import *
import time

def add_text_to_text_edit(text):
	print(text)

gatewayConfig = json.load(open("configs/gatewayConfig.json"))
fb.flash_procedure(gatewayConfig["firmwareVersion"], gatewayConfig["gatewayVersion"], add_text_to_text_edit)
