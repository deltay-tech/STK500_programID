# STK500 Tool for production programming
### Programming AVR MCU with EEPROM ID serialization  
## Features

![](/DOC/mainwindow.PNG) 

ID (4 bytes) in EEPROM at address from 0 to 4
Byteorder Hi to Lo, 0x12345678 - > address:value 00:12, 01:34, 02:56, 03:78
ID managed by SQLite DB with info about programming time

## Setup
OS: Windows

Put your flash firmware hex image file:
| [ProgramID/firmware/flash.hex](ProgramID/firmware/flash.hex) |

Setup STK500 programing line (STK500.exe path and parameters) for your specific chip and config:
| [ProgramID/settings/programchip.txt](ProgramID/settings/programchip.txt)) |

## Setup Python Modules
Additional Python Modules required: 
PyQt5, IntelHex, pyinstaller 

## Build
Prepare pack release:
Run |[ProgramID/pack2exe.bat](ProgramID/pack2exe.bat)) |

## Run
Run after pack:
|ProgramID/dist/programID/programID.exe|

## DB managment
Create new clear db 
(ID starts with 00000001)
! Manually delete IDdatabase.db first!:
Run |[ProgramID/database/createBD.bat](ProgramID/database/createBD.bat)|


