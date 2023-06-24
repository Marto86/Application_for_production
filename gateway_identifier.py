import time
import serial
import subprocess
import os
import os.path
import re

class GatewayIdentifier:
    def __init__(self, debug=False, port=None):
        # self._logger = logging.getLogger('EspController')
        self.debug = debug
        self._bin_dir = f'bin{os.sep}'
        self._firmware_v2_dir = f'firmware_v2{os.sep}'
        self._serial = serial.Serial()
        self._serial.baudrate = 115200
        self._serial.bytesize = 8
        self._serial.parity = serial.PARITY_NONE
        self._serial.stopbits = 1
        self._serial.timeout = 3
        if port is not None:
            self._port = port
            self._serial.port = port
        else:
            self._find_port()

    def _find_port(self):
        (success, df) = run_safe()(subprocess.check_output)("ls /dev/serial/by-id/", shell=True)
        if not success:
            self._port = '/dev/ttyUSB0'
            self._serial.port = '/dev/ttyUSB0'
            self._logger.warning('Fail to detect CP2102 port')
            return
        for byte_line in df.split(b'\n'):
            line = byte_line.decode('utf-8')
            if byte_line and 'CP2102' in line:
                self._port = f'/dev/serial/by-id/{line}'
                self._serial.port = self._port
                if self.debug:
                    print(f'Port={self._port}')
                return
        self._port = '/dev/ttyUSB0'
        self._serial.port = '/dev/ttyUSB0'

    def _boot_sequence(self):
        self._serial._dtr_state = False
        self._serial._rts_state = True
        self._serial._reconfigure_port()
        time.sleep(0.5)
        self._serial._dtr_state = True
        self._serial._rts_state = False
        self._serial._reconfigure_port()
        time.sleep(0.5)
        self._serial.setDTR(False)

    def _reset_sequence(self):
        self._serial.setDTR(False)
        self._serial.setRTS(True)
        time.sleep(0.1)
        self._serial.setRTS(False)

    def get_serial_num(self, text):
        pattern = 'GWID_SN:(.*)'
        result = re.search(pattern, text)
        return result.groups(1)[0]

    def get_firmware_version(self, text):
        pattern = 'GWID_Firmware:(.*)'
        result = re.search(pattern, text)
        return result.groups(1)[0]
    
    def get_gwuuid(self, text):
        pattern = 'GWID_UUID:(.*)'
        result = re.search(pattern, text)
        return result.groups(1)[0]

    def get_imei(self, lines, idx):
        return lines[idx+1].strip()

    def get_sim_sn(self, lines, idx):
        return lines[idx+1].strip()
    
    def get_sim_iccid(self, lines, idx):
        return lines[idx+1].strip()

    def get_info(self):
        try:
            lines = []
            self._serial.open()
            start_time = time.time()

            gwsn_row = None
            gwfw_row = None
            gwuuid_row = None
            gwimei_idx = None
            gwsimsn_idx = None
            gwccid_idx = None
            counter = 0
            is_4g = None
            imei = None
            sim_serial_number = None
            modbus_working = False
            while True:
                line_def = self._serial.readline()
                line = line_def.decode('utf-8', errors='ignore')
                
                lines.append(line)

                if("GWMODBUS_WORKING" in line):
                    modbus_working = True

                if("GWID_SN" in line):
                    gwsn_row = line

                if("GWID_Firmware" in line):
                    gwfw_row = line

                if("GWID_UUID" in line):
                    gwuuid_row = line

                if("GWID_IMEI" in line):
                    gwimei_idx = counter

                if("GWID_SIMSN" in line):
                    gwsimsn_idx = counter
                
                if("GWID_CCID" in line):
                    gwccid_idx = counter

                if("GWID_IS4G:NO" in line):
                    is_4g = False
                    break;

                if("GWID_IS4G:YES" in line):
                    is_4g = True

                #Break 5 rows after SIM serial number is found
                if(gwsimsn_idx is not None and counter > gwsimsn_idx+5):
                    break;
                
                if(time.time() - start_time > 20):
                    break;

                counter = counter + 1

            serial_number = None
            firmware_version = None
            gwuuid = None
            if(gwsn_row is not None and gwfw_row is not None and gwuuid_row is not None):
                serial_number = self.get_serial_num(gwsn_row.replace('\x1b[0;32m', '').replace('\x1b[0m', '').strip())
                firmware_version = self.get_firmware_version(gwfw_row.replace('\x1b[0;32m', '').replace('\x1b[0m', '').strip())
                gwuuid = self.get_gwuuid(gwuuid_row.replace('\x1b[0;32m', '').replace('\x1b[0m', '').strip())
            if(is_4g):
                imei = self.get_imei(lines, gwimei_idx)
                sim_iccid_number_at = self.get_sim_iccid(lines, gwccid_idx)
                sim_iccid_number_split = str(sim_iccid_number_at).split()
                sim_iccid_number = sim_iccid_number_split[1]
            if is_4g and (imei is None or sim_iccid_number is None):
                raise Exception("IMEI or SIM CCID not found in the serial output!")
            
            return serial_number, firmware_version, imei, sim_iccid_number, gwuuid, is_4g, modbus_working
        except Exception as error:
            #self._logger.error('identification', exc_info=True)
            print(error)
        finally:
            self._serial.close()

        return None, '0.0'
        
