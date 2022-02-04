from PyQt5 import QtWidgets,uic
from PyQt5.QtCore import Qt
from mainwindow import *
import sys,subprocess,io,os
from intelhex import IntelHex
import sqlite3, datetime, shutil

conn = sqlite3.connect("database\IDdatabase.db")
cursor = conn.cursor()

#devices types
devicesSet=["Reserved","Exported","Programmed"] 
#STK500 response list
correctSTKresponse=["FLASH verified successfully","EEPROM verified successfully","Fuse bits verified successfully","Lock bits verified successfully"]

def readArg():
    lineProgram=open('settings\programchip.txt');
    arglineraw=lineProgram.read()
    lineProgram.close()
    searchFile='Stk500.exe'
    curPath = os.getcwd()+"\\firmware\\"
    argline=arglineraw.replace("?",curPath)
    pathSTK=argline[:argline.index(searchFile)+len(searchFile)]
    pathParam=argline[argline.index(searchFile)+len(searchFile):]
    paramout=pathParam.split(' ')
    paramout[0]=pathSTK;
    return paramout

def prepareEEPROM(serialID):
    ih = IntelHex()
    ih.puts(0x0,serialID.to_bytes(4, byteorder='big'))
    ih.write_hex_file("firmware\\eeprom.hex")

def getLastIdData():
    """Returns last db data: 0 - id, 1- time, 2-devicetype"""
    sqlLast = "SELECT id,programtime,devicetype FROM IDs ORDER by id DESC LIMIT 1"
    cursor.execute(sqlLast)
    lastData=cursor.fetchall()
    return lastData[0]
    
def insertID(idLast,deviceType):
    newid=idLast+1
    sqlNew = "INSERT INTO 'IDs' VALUES('{}','{}','{}')".format(newid, str(datetime.datetime.now())[:-7], deviceType)
    cursor.execute(sqlNew)
    conn.commit()

def programChip():
    proc = subprocess.Popen(stkarg,stdout=subprocess.PIPE)
    outlines=[]
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        strline=line.rstrip().decode("utf-8")
        outlines.append(strline)
    return outlines
        
class porgramWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(porgramWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.programmOk.clicked.connect(self.confirmMarking)
        self.ui.programmButton.clicked.connect(self.programDevice)
        self.ui.exportAddress.clicked.connect(self.exportAddressToFile)
        self.setWindowIcon(QtGui.QIcon('app\chip.ico'))
        self.ui.programmOk.setEnabled(False)

    def programDevice(self):
        valResult=getLastIdData()
        prepareEEPROM(int(valResult[0])+1)
        self.ui.logdata.setPlainText("")    
        self.ui.currentID.setText("")  
        self.ui.programmResult.setText("") 
        self.ui.programmResult.setStyleSheet("color: rgb(0, 0, 0);")
        app.processEvents() 
        #execute STK500
        logtext="\r\n".join(programChip())
        self.ui.logdata.setPlainText(logtext)
        #check log
        correctIndex=0
        for checkResponse in correctSTKresponse:
            if checkResponse in logtext:
                correctIndex+=1
        if correctIndex==len(correctSTKresponse):
            self.ui.programmButton.setEnabled(False)
            self.ui.programmOk.setEnabled(True)
            self.ui.lastID.setText(f'{(int(valResult[0])+1):0>8X}')    
            self.ui.currentID.setText(f'{(int(valResult[0])+1):0>8X}')          
            self.ui.programmResult.setText("Programmed successfully!") 
            self.ui.programmResult.setStyleSheet("color: rgb(0, 127, 0);")
            insertID(int(valResult[0]),2)
        else:
            self.ui.programmResult.setText("Error!") 
            self.ui.programmResult.setStyleSheet("color: rgb(127, 0, 0);")
            
    def confirmMarking(self):
        self.ui.programmButton.setEnabled(True)
        self.ui.programmOk.setEnabled(False)
        self.ui.programmResult.setText("") 
        self.ui.logdata.setPlainText("")  
        self.ui.currentID.setText("")
        self.ui.programmResult.setStyleSheet("color: rgb(0, 0, 0);")
        self.updateValues(getLastIdData())
        
    def updateValues(self, inputValues):   
        self.ui.lastID.setText(f'{inputValues[0]:0>8X}') 
        self.ui.lastTime.setText(inputValues[1])
        self.ui.deviceType.setText(devicesSet[inputValues[2]]) 
        app.processEvents() 
        
    def exportAddressToFile(self):
        exportCount=self.ui.addressQnt.value()    
        if exportCount>0:
            savePath = QtWidgets.QFileDialog.getSaveFileName(application, "Save file with addresses", '/', '.txt')
            fileName=''.join(savePath)
            if len(fileName)>4:
                saveFile=open(fileName,"w")
                saveFile.write("File with addresses\nDate:{}".format(str(datetime.datetime.now())[:-7]))
                saveFile.write("\nQuantity:{}\n".format(exportCount))
                for i in range (exportCount):
                    valExport=getLastIdData()
                    insertIDval=int(valExport[0])+1
                    saveFile.write(f'{insertIDval:0>8X}'+"\n")
                    insertID(int(valExport[0]),1)
                saveFile.close()
                shutil.copyfile(fileName, "exports\{}".format(fileName[fileName.rfind("/")+1:]))
                self.updateValues(getLastIdData())
            self.ui.addressQnt.setValue(0)
            
    def keyPressEvent(self, e):
        if e.key()==Qt.Key_F9:
            self.programDevice()
        elif e.key()==Qt.Key_F10:
            self.confirmMarking()
        
app = QtWidgets.QApplication([])
application = porgramWindow()
application.show()
stkarg=readArg()
application.updateValues(getLastIdData())
sys.exit(app.exec())