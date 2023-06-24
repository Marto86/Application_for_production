Flashing tool instructions 
Step 1.
Execute all steps from: https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/get-started/linux-macos-setup.html#
to install sucsesfully idf environment
step 3.install esp tools package 
execute commant in linux terminal : pip install esptool



Command in windows 
1 install.bat
2 python C:\Espressif\frameworks\esp-idf-v4.4\components\nvs_flash\nvs_partition_generator\nvs_partition_gen.py generate provisioning\provisioning.csv provisioning\provisioning.bin 0x4000
3 python C:\Espressif\frameworks\esp-idf-v4.4\components\partition_table\parttool.py --port COM3 write_partition --partition-name=provisioning --input provisioning\provisioning.bin



