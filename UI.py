from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QPlainTextEdit,
    QVBoxLayout,
    QWidget,
)
from sympy import true
import tb_flash_board
from PyQt5.QtCore import QProcess
from PyQt5 import QtCore, QtGui, QtWidgets
import tb_flash_board as fb
import sys
import subprocess as sb
import gateway_identifier
import json
from cloud_ingeli_registerer import *
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import registration_helper as rh

class Ui_MainWindow(object):
    def __init__(self):
        self.deviceType = None

    def show_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Select Gateway Type")
        msg.setText("Choose Gateway device type!")
        msg.setIcon(QMessageBox.Question)
        # msg.setStandardButtons(QMessageBox.Cancel|QMessageBox.Retry|QMessageBox.Ignore)
        msg.addButton('4G', QtWidgets.QMessageBox.YesRole)
        msg.addButton('WiFi', QtWidgets.QMessageBox.NoRole)
        msg.setBaseSize(600, 300)
        msg.buttonClicked.connect(self.popup_button_clicked)
        msg.exec()

    def popup_button_clicked(self, i):
        self.deviceType = i.text()

    def add_text_to_text_edit(self, text):
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(str(text))
        cursor.movePosition(cursor.End)
        self.textBrowser.ensureCursorVisible()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1295, 720)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.flashButton = QtWidgets.QPushButton(self.centralwidget)
        self.flashButton.setGeometry(QtCore.QRect(0, 360, 350, 331))
        self.flashButton.setStyleSheet(
            "QPushButton"
            "{"
            "background-color : green;"
            "}"
            "QPushButton::pressed"
            "{"
            "background-color : #be0000;"
            "}"
        )
        font = QtGui.QFont()
        font.setPointSize(36)
        self.flashButton.setFont(font)
        self.flashButton.setMouseTracking(True)
        self.flashButton.setTabletTracking(True)
        self.flashButton.setObjectName("flashButton")

        self.confirmDeviceButton = QtWidgets.QPushButton(self.centralwidget)
        self.confirmDeviceButton.setGeometry(QtCore.QRect(350, 360, 305, 331))
        self.confirmDeviceButton.setStyleSheet(
            "QPushButton"
            "{"
            "background-color : orange;"
            "}"
            "QPushButton::pressed"
            "{"
            "background-color : #be0000;"
            "}"
        )
        font2 = QtGui.QFont()
        font2.setPointSize(36)
        self.confirmDeviceButton.setFont(font2)
        self.confirmDeviceButton.setMouseTracking(True)
        self.confirmDeviceButton.setTabletTracking(True)
        self.confirmDeviceButton.setObjectName("confirmDeviceButton")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(660, 0, 621, 221))
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setFrameShape(QtWidgets.QFrame.HLine)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("label.PNG"))
        self.label.setScaledContents(True)
        self.label.setIndent(-2)
        self.label.setObjectName("label")
        self.printButton = QtWidgets.QPushButton(self.centralwidget)
        self.printButton.setGeometry(QtCore.QRect(655, 360, 275, 331))
        self.printButton.setStyleSheet(
            "QPushButton"
            "{"
            "background-color : yellow;"
            "}"
            "QPushButton::pressed"
            "{"
            "background-color : #be0000;"
            "}"
        )
        font = QtGui.QFont()
        font.setPointSize(36)
        self.printButton.setFont(font)
        self.printButton.setMouseTracking(True)
        self.printButton.setTabletTracking(True)
        self.printButton.setObjectName("printButton")
        self.modbusStatusLabel = QtWidgets.QLabel(self.centralwidget)
        self.modbusStatusLabel.setGeometry(QtCore.QRect(930, 360, 361, 171))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.modbusStatusLabel.setFont(font)
        self.modbusStatusLabel.setMouseTracking(True)
        self.modbusStatusLabel.setTabletTracking(True)
        self.modbusStatusLabel.setObjectName("modbusStatusLabel")
        self.modbusStatusLabel.setStyleSheet(
            "QLabel"
            "{"
            "background-color : gray;"
            "}"
        )
        self.modbusStatusLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.shutDownButton = QtWidgets.QPushButton(self.centralwidget)
        self.shutDownButton.setGeometry(QtCore.QRect(930, 530, 361, 161))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.shutDownButton.setFont(font)
        self.shutDownButton.setMouseTracking(True)
        self.shutDownButton.setTabletTracking(True)
        self.shutDownButton.setObjectName("shutDownButton")
        self.shutDownButton.setStyleSheet("background-color : #580000")
        (
            "QPushButton"
            "{"
            "background-color : #580000;"
            "}"
            "QPushButton::pressed"
            "{"
            "background-color : #000000;"
            "}"
        )
        self.statusLabel = QtWidgets.QLabel(self.centralwidget)
        self.statusLabel.setGeometry(QtCore.QRect(660, 230, 631, 131))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.statusLabel.setFont(font)
        self.statusLabel.setScaledContents(True)
        self.statusLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.statusLabel.setObjectName("statusLabel")
        self.textBrowser = QtWidgets.QTextEdit(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(-5, 1, 661, 361))
        self.textBrowser.setObjectName("textBrowser")
        self.label.raise_()
        self.flashButton.raise_()
        self.printButton.raise_()
        self.modbusStatusLabel.raise_()
        self.shutDownButton.raise_()
        self.statusLabel.raise_()
        self.textBrowser.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1295, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.printButton.clicked.connect(self.print_label)
        self.flashButton.clicked.connect(self.flash_firmware)
        self.confirmDeviceButton.clicked.connect(self.confirm_device)
        #  self.modbusStatusLabel.clicked.connect(self.reboot)
        self.shutDownButton.clicked.connect(self.shut_down)
        self.label.update()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.textBrowser.clear()
        self.statusLabel.clear()
        self.label.clear()

    def print_label(self):
        self._confirm_device_internal(True)
        # serial_number = fb.get_last_flashed_serial_number()
        # fb.print_label(serial_number)
        # fb.print_4G_label(serial_number,imei,sim_iccid_number)
        # self.label.setPixmap(QtGui.QPixmap("label.PNG"))

    def flash_firmware(self):
        try:
            self.textBrowser.clear()
            self.statusLabel.clear()
            self.label.clear()
            self.statusLabel.setText("Flashing...")
            gatewayConfig = json.load(open("configs/gatewayConfig.json"))
            if True == fb.flash_procedure(gatewayConfig["firmwareVersion"], gatewayConfig["gatewayVersion"], self.add_text_to_text_edit):
                self.statusLabel.setStyleSheet("background-color: lightgreen")
                self.statusLabel.setText("Flashed successfully")
                #self.label.setPixmap(QtGui.QPixmap("label.PNG"))
            else:
                self.statusLabel.setStyleSheet("background-color: red")
                self.statusLabel.setText("Failed to flash")
            self.textBrowser.setReadOnly(True)
        except Exception as e:
            self.statusLabel.setStyleSheet("background-color: red")
            self.statusLabel.setText("Failed to flash")
            self.add_text_to_text_edit(str(e))
            #self.textBrowser.insertPlainText(str(e))

    def confirm_device(self):
        self._confirm_device_internal()

    def _confirm_device_internal(self, force_print=False):
        self.statusLabel.setText("Confirming...")
        gateway_config = json.load(open("configs/gatewayConfig.json"))
        gw_identifier = gateway_identifier.GatewayIdentifier(True, gateway_config["usb"])
        serial_number = None
        gwuuid = None
        firmware_version = None
        imei = None
        sim_iccid_number = None
        is4g = None
        modbus_working = None
        serial_number, firmware_version, imei, sim_iccid_number, gwuuid, is4g, modbus_working = gw_identifier.get_info()
        ingeli_config = json.load(open("configs/ingeliConfig.json"))
        request = {"id": ingeli_config["token"], "firmwareVersion": firmware_version, "hardwareVersion": gateway_config["gatewayVersion"], "uuid": gwuuid}
        
        if(modbus_working):
            self.modbusStatusLabel.setStyleSheet("background-color: green")
            self.modbusStatusLabel.setText("RS485 OK")
        else:
            self.modbusStatusLabel.setStyleSheet("background-color: red")
            self.modbusStatusLabel.setText("RS485 Error")

        if(is4g is None or serial_number is None or firmware_version is None or gwuuid is None):
            self.statusLabel.setStyleSheet("background-color: red")
            self.statusLabel.setText("Not recognized!Try again!")
            return
            
        if(is4g and self.deviceType == 'WiFi'):
            self.statusLabel.setStyleSheet("background-color: red")
            self.statusLabel.setText("WiFi device expected!(Not 4G)")
            return
        elif(is4g is False and self.deviceType == '4G'):
            self.statusLabel.setStyleSheet("background-color: red")
            self.statusLabel.setText("4G device expected!(Not WiFi)")
            return

        if(is4g and imei is not None and sim_iccid_number is not None):
            request["imei"] = imei
            request["iccid"] = sim_iccid_number
        
        registerer = CloudIngeliRegisterer(ingeli_config["provisioningApiUrl"],ingeli_config["token"]) #class to do request<<<<<
        is_confirmed_by_api = registerer.confirm_register(request, self.add_text_to_text_edit)
        if(is_confirmed_by_api):
            self.statusLabel.setStyleSheet("background-color: green")
            self.statusLabel.setText("Force print done" if force_print else "Confirmed successfully")
            if(is4g and imei is not None and sim_iccid_number is not None and self.deviceType == '4G'):
                fb.print_4G_label(serial_number,imei,sim_iccid_number)
                self.label.setPixmap(QtGui.QPixmap("label.PNG"))
                rh.remove_reg_info_json(serial_number)
            if(self.deviceType == 'WiFi'):
                fb.print_label(serial_number)
                self.label.setPixmap(QtGui.QPixmap("label.PNG"))
                rh.remove_reg_info_json(serial_number)
        else:
            self.statusLabel.setStyleSheet("background-color: red")
            self.statusLabel.setText("Failed to confirm")

    def shut_down(self):
        sb.run("poweroff", shell=True)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Ingeli Tool"))
        self.flashButton.setText(_translate("MainWindow", "Flash"))
        self.confirmDeviceButton.setText(_translate("MainWindow", "Confirm"))
        self.printButton.setText(_translate("MainWindow", "Force \nPrint"))
        # self.modbusStatusLabel.setText(_translate("MainWindow", ""))
        self.shutDownButton.setText(_translate("MainWindow", "Shut down"))
        self.statusLabel.setText(_translate("MainWindow", "PASS"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.show_popup()

    if(ui.deviceType is not None):
        MainWindow.show()
        app.exec_()
        sys.exit()



