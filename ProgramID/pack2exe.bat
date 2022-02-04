pyinstaller --noconsole programID.py -i "app\chip.ico"
mkdir dist\programID\exports
mkdir dist\programID\firmware
mkdir dist\programID\settings
mkdir dist\programID\database
mkdir dist\programID\app
copy firmware\* dist\programID\firmware
copy database\* dist\programID\database
copy settings\* dist\programID\settings
copy app\* dist\programID\app
mkdir dist\programID\app