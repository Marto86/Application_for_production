import requests
import json
import logging


class RegistrationInfos:
    def __init__(self, uuid, serial_number, sector, login, password):
        self.uuid = uuid
        self.serial_number = serial_number
        self.sector = sector
        self.login = login
        self.password = password


class CloudIngeliRegisterer:
    def __init__(self, base_url, token):
        self._base_url = base_url
        self._token = token
        self._logger = logging.getLogger('Registerer')

    def is_connected(self):
        try:
            self._logger.error('is_connected')
            response = requests.post(self._base_url + 'status', json={"id": self._token}, verify=False, timeout=10)
            if response.status_code == 200:
                return True, response.content.decode('utf-8', errors='ignore')
            elif response.status_code == 400:
                return False, response.content.decode('utf-8', errors='ignore')
            return False, 'NOT CONNECTED'
        except Exception as _:
            self._logger.error('is_connected', exc_info=True)
            return False, 'NOT CONNECTED'

    def try_register(self, firmware_version, hardware_version, uuid=None) -> (bool, RegistrationInfos):
        try:
            response = requests.post(self._base_url + 'register-request', json={"id": self._token, "firmwareVersion": firmware_version, "hardwareVersion": hardware_version}, verify=False, timeout=10) if uuid is None\
                else requests.post(self._base_url + 'get-non-production', json={"id": self._token, "firmwareVersion": firmware_version, "hardwareVersion": hardware_version, "uuid": uuid}, verify=False, timeout=10)
            if response.status_code != 200:
                return False, None

            registration_infos_json = json.loads(response.content.decode('utf-8'))
            infos = RegistrationInfos(registration_infos_json['uuid'], registration_infos_json['serialNumber'], registration_infos_json['sector'], registration_infos_json['login'], registration_infos_json['password'])
            return True, infos
        except KeyError as key_error:
            self._logger.error(f'try_register : Key not found : {str(key_error)}')
            return False, None
        except Exception as _:
            self._logger.error('try_register', exc_info=True)
            return False, None

    def confirm_register(self, confirmation, log_callback):
        try:
            confirmation["id"] = self._token
            response = requests.post(self._base_url + 'confirm-register', json=confirmation, verify=False, timeout=10)
            log_callback(response.content)
            return response.status_code == 200 or ("already registered" in response.content.decode())
        except Exception as ex:
            log_callback(str(ex))
            self._logger.error('confirm_register', exc_info=True)
            return False


if __name__ == '__main__':
    registerer2 = CloudIngeliRegisterer('https://provisioning.polytropic.ingelink.dev/polyconnectgatewaz/', '97a9e2dda348bcb89dba615fc64acbb7a0382287a0285c357b005383e6605b16')
    print(f'connected : {registerer2.is_connected()}')
    registerer2 = CloudIngeliRegisterer('https://provisioning.polytropic.ingelink.dev/polyconnectgateway/', 'badToken')
    print(f'connected : {registerer2.is_connected()}')
    registerer2 = CloudIngeliRegisterer('https://provisioning.polytropic.ingelink.dev/polyconnectgateway/', '97a9e2dda348bcb89dba615fc64acbb7a0382287a0285c357b005383e6605b16')
    print(f'connected : {registerer2.is_connected()}')

