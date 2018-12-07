
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLineEdit, QDialog, 
                             QVBoxLayout, QAction, QMessageBox, QComboBox, 
                             QLabel,QSplitter,QPushButton,QTableWidget,QWidget,
                             QSpacerItem, QInputDialog, QFileDialog, QTableWidgetItem)
from PyQt5.QtCore import (QT_VERSION_STR, PYQT_VERSION_STR,pyqtSignal)
from PyQt5.QtCore import Qt
from PyQt5.Qt import QGridLayout, QHBoxLayout

from PyQt5 import QtCore, QtGui, QtWidgets
import platform
import sys



WHEAT_CHROMOSOMES = [
    "chr1A",
    "chr2A",
    "chr3A",
    "chr4A",       
    "chr5A",
    "chr6A",  
    "chr7A",    
    "chr1B",
    "chr2B",
    "chr3B",
    "chr4B",        
    "chr5B",
    "chr6B",  
    "chr7B",        
    "chr1D",
    "chr2D",
    "chr3D",
    "chr4D",        
    "chr5D",
    "chr6D",   
    "chr7D",

]
GUI_CONFIG = {
    "combo_box_size": 250,
    "input_size": 99,
    "search_size": 242,
    "query_size": 143,
    "TagLenG1":10,
    "TagLenG2":10,
    "headerlabels": "ID;CHR;POS;Q;SEQ;"
}

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('Visual Tag Analyzer') 

        
        # Create the File menu
        self.menuFile = self.menuBar().addMenu("&File")
        self.actionImport = QAction("&Import Genome Tags", self)
        self.actionImport.triggered.connect(self.importgtags)
        self.actionQuit = QAction("&Quit", self)
        self.actionQuit.triggered.connect(self.close)
        self.menuFile.addActions([self.actionImport, self.actionQuit])
        
        # Create the Help menu
        self.menuHelp = self.menuBar().addMenu("&Help")
        self.actionAbout = QAction("&About",self)
        self.actionAbout.triggered.connect(self.about)
        self.menuHelp.addActions([self.actionAbout])
        
        # Setup main widget
        self.widget = QDialog()
        self.widget.move(50,50)
        self.genome1 = QComboBox()
        self.genome1.addItem("Genome 1: None")
        self.genome1.setFixedWidth(GUI_CONFIG["combo_box_size"])
        
        self.genome2 = QComboBox()
        self.genome2.addItem("Genome 2: None")
        self.genome2.setFixedWidth(GUI_CONFIG["combo_box_size"])
        
        self.chromosome1 = QComboBox()
        self.chromosome1.addItem("Chromosome 1: None")
        for chromosome in WHEAT_CHROMOSOMES:
            self.chromosome1.addItem(chromosome)
        self.chromosome1.setFixedWidth(GUI_CONFIG["combo_box_size"])       
        
        self.chromosome2 = QComboBox()
        self.chromosome2.addItem("Chromosome 2: None")
        for chromosome in WHEAT_CHROMOSOMES:
            self.chromosome2.addItem(chromosome)
        self.chromosome2.setFixedWidth(GUI_CONFIG["combo_box_size"])          
        
        self.rangefrom1 = QLineEdit("")
        self.rangefrom1.setFixedWidth(GUI_CONFIG["input_size"])
        self.rangeto1 = QLineEdit("")
        self.rangeto1.setFixedWidth(GUI_CONFIG["input_size"]+1)
        self.rangefrom2 = QLineEdit("")
        self.rangefrom2.setFixedWidth(GUI_CONFIG["input_size"]-1)
        self.rangeto2 = QLineEdit("")
        self.rangeto2.setFixedWidth(GUI_CONFIG["input_size"])
        
        self.searcher = QLineEdit("")
        self.searcher.setFixedWidth(GUI_CONFIG["search_size"])
        
        self.searchlabel = QLabel("Search tags on screen:")
        self.searchlabel.setBuddy(self.searcher)
       
        self.SearchButton = QPushButton("Analyze Query")
        self.SearchButton.setFixedWidth(GUI_CONFIG["query_size"])
        self.SearchButton.setDefault(True)
        self.SearchButton.clicked.connect(self.filereader)
        
        fromLabel1 = QLabel("From")
        fromLabel1.setBuddy(self.rangefrom1)
        
        toLabel1 = QLabel("to")
        toLabel1.setBuddy(self.rangeto1)
        
        fromLabel2 = QLabel("From")
        fromLabel2.setBuddy(self.rangefrom2)
        
        toLabel2 = QLabel("to")
        toLabel2.setBuddy(self.rangeto2)
      
        toplayout = QHBoxLayout()
        toplayout.addWidget(self.genome1)
        toplayout.addWidget(self.genome2)
        toplayout.addStretch(1)
        
        midlayout = QHBoxLayout()
        midlayout.addWidget(self.chromosome1)
        midlayout.addWidget(self.chromosome2)
        midlayout.addStretch(1)
                
        botlayout = QHBoxLayout()
        botlayout.addWidget(fromLabel1)
        botlayout.addWidget(self.rangefrom1)
        botlayout.addWidget(toLabel1)
        botlayout.addWidget(self.rangeto1)
        botlayout.addWidget(fromLabel2)
        botlayout.addWidget(self.rangefrom2)
        botlayout.addWidget(toLabel2)
        botlayout.addWidget(self.rangeto2)
        botlayout.addStretch(1)

        searchlayout = QHBoxLayout()
        searchlayout.addWidget(self.searchlabel)
        searchlayout.addWidget(self.searcher)
        searchlayout.addWidget(self.SearchButton)
        searchlayout.addStretch(1)  

        
        self.tableWidget1 = QTableWidget(0, 5)
        self.tableWidget2 = QTableWidget(0, 5)
        self.tableWidget1.setHorizontalHeaderLabels((GUI_CONFIG["headerlabels"]).split(";"))
        self.tableWidget2.setHorizontalHeaderLabels((GUI_CONFIG["headerlabels"]).split(";"))
        self.tableWidget1.resizeColumnsToContents()
        self.tableWidget2.resizeColumnsToContents()

        self.viewerlayout = QHBoxLayout()
        self.viewerlayout.addWidget(self.tableWidget1)
        self.viewerlayout.addWidget(self.tableWidget2)
        self.setLayout(self.viewerlayout)
 

        self.layout = QVBoxLayout()
        self.layout.addLayout(toplayout)
        self.layout.addLayout(midlayout)
        self.layout.addLayout(botlayout)
        self.layout.addSpacerItem(QSpacerItem(0, 10))
        self.layout.addLayout(searchlayout)
        self.layout.addLayout(self.viewerlayout)

          
        self.widget.setLayout( self.layout)
        self.setCentralWidget(self.widget)
        self.setGeometry(725, 350, 0, 500)

    def importgtags(self):   
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Import Genome Tags", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            f= str(fileName)
            self.genome1.addItem(f)
            self.genome2.addItem(f)

    def filereader(self):

        genomename1 = str(self.genome1.currentText())
        genomename2 = str(self.genome2.currentText())
        if genomename1 != "Genome 1: None": data1 = (open(genomename1,"r")).readlines()
        if genomename2 != "Genome 2: None": data2 = (open(genomename2,"r")).readlines()



        list1_ID = []
        list1_CHR = []
        list1_POS = []
        list1_Q = []
        list1_SEQ = []
        list1_index = []
        list1_index2 = []
        list2_ID = []
        list2_CHR = []
        list2_POS = []
        list2_Q = []
        list2_SEQ=  []
        list2_index = []
        list2_index2 = []

        if genomename1 != "Genome 1: None":

            for x in data1:
                list1_CHR.append(x.split(' ')[1])
            if self.chromosome1.currentText() != "Chromosome 1: None":
                for ind, CHR in enumerate(list1_CHR, start=0):
                    if CHR == str(self.chromosome1.currentText()): 
                        list1_index.append(ind)
                list1_CHR = []

                if (self.rangefrom1.text() != "" and self.rangeto1.text() != ""):

                    for ind, x in enumerate(data1):
                        if ind in list1_index:
                            if (int(x.split(' ')[2]) >= (int(self.rangefrom1.text()) - int(len(x.split(' ')[4]))) and int(x.split(' ')[2]) <= (int(self.rangeto1.text()))):
                                list1_index2.append(ind)
                                
                    GUI_CONFIG["TagLenG1"] = len(list1_index2)
                    self.tableWidget1.setRowCount(GUI_CONFIG["TagLenG1"])
                    for ind,x in enumerate(data1):
                        if ind in list1_index2:
                            print("It's working!!")
                            list1_ID.append(x.split(' ')[0])
                            list1_CHR.append(x.split(' ')[1])
                            list1_POS.append(x.split(' ')[2])
                            list1_Q.append(x.split(' ')[3])
                            list1_SEQ.append(x.split(' ')[4])
                else:
                    GUI_CONFIG["TagLenG1"] = len(list1_index)
                    self.tableWidget1.setRowCount(GUI_CONFIG["TagLenG1"])
                    for ind,x in enumerate(data1):
                        if ind in list1_index:
                            list1_ID.append(x.split(' ')[0])
                            list1_CHR.append(x.split(' ')[1])
                            list1_POS.append(x.split(' ')[2])
                            list1_Q.append(x.split(' ')[3])
                            list1_SEQ.append(x.split(' ')[4])
                
            else:
                GUI_CONFIG["TagLenG1"] = len(data1)
                print("data1",len(data1))
                self.tableWidget1.setRowCount(GUI_CONFIG["TagLenG1"])

                for x in data1:
                    list1_ID.append(x.split(' ')[0])
                    list1_CHR.append(x.split(' ')[1])
                    list1_POS.append(x.split(' ')[2])
                    list1_Q.append(x.split(' ')[3])
                    list1_SEQ.append(x.split(' ')[4])

            for col,ID in enumerate(list1_ID, start=0):
                self.tableWidget1.setItem(col,0,QTableWidgetItem(ID))
            for col,CHR in enumerate(list1_CHR, start=0):
                self.tableWidget1.setItem(col,1,QTableWidgetItem(CHR))        
            for col,POS in enumerate(list1_POS, start=0):
                self.tableWidget1.setItem(col,2,QTableWidgetItem(POS))
            for col,Q in enumerate(list1_Q, start=0):
                self.tableWidget1.setItem(col,3,QTableWidgetItem(Q))  
            for col,SEQ in enumerate(list1_SEQ, start=0):
                self.tableWidget1.setItem(col,4,QTableWidgetItem(SEQ))  
                    
        if genomename2 != "Genome 2: None":        

            for x in data2:
                list2_CHR.append(x.split(' ')[1])
            if self.chromosome2.currentText() != "Chromosome 2: None":
                for ind, CHR in enumerate(list2_CHR, start=0):
                    if CHR == str(self.chromosome2.currentText()): 
                        list2_index.append(ind)
                list2_CHR = []

                if (self.rangefrom2.text() != "" and self.rangeto2.text() != ""):
                    for ind, x in enumerate(data2):
                        if ind in list2_index:
                            if (int(x.split(' ')[2]) >= (int(self.rangefrom2.text()) - int(len(x.split(' ')[4]))) and int(x.split(' ')[2]) <= (int(self.rangeto2.text()))):
                                list2_index2.append(ind)

                    GUI_CONFIG["TagLenG2"] = len(list2_index)
                    self.tableWidget2.setRowCount(GUI_CONFIG["TagLenG2"])
                    for ind,x in enumerate(data2):
                        if ind in list2_index2:
                            list2_ID.append(x.split(' ')[0])
                            list2_CHR.append(x.split(' ')[1])
                            list2_POS.append(x.split(' ')[2])
                            list2_Q.append(x.split(' ')[3])
                            list2_SEQ.append(x.split(' ')[4])
                else:
                    GUI_CONFIG["TagLenG2"] = len(list2_index)
                    self.tableWidget2.setRowCount(GUI_CONFIG["TagLenG2"])
                    for ind,x in enumerate(data2):
                        if ind in list2_index:
                            list2_ID.append(x.split(' ')[0])
                            list2_CHR.append(x.split(' ')[1])
                            list2_POS.append(x.split(' ')[2])
                            list2_Q.append(x.split(' ')[3])
                            list2_SEQ.append(x.split(' ')[4])
                
            else:
                GUI_CONFIG["TagLenG2"] = len(data2)
                print("data2",len(data2))
                self.tableWidget2.setRowCount(GUI_CONFIG["TagLenG2"])

                for x in data2:
                    list2_ID.append(x.split(' ')[0])
                    list2_CHR.append(x.split(' ')[1])
                    list2_POS.append(x.split(' ')[2])
                    list2_Q.append(x.split(' ')[3])
                    list2_SEQ.append(x.split(' ')[4])

            for col,ID in enumerate(list2_ID, start=0):
                self.tableWidget2.setItem(col,0,QTableWidgetItem(ID))
            for col,CHR in enumerate(list2_CHR, start=0):
                self.tableWidget2.setItem(col,1,QTableWidgetItem(CHR))        
            for col,POS in enumerate(list2_POS, start=0):
                self.tableWidget2.setItem(col,2,QTableWidgetItem(POS))
            for col,Q in enumerate(list2_Q, start=0):
                self.tableWidget2.setItem(col,3,QTableWidgetItem(Q))  
            for col,SEQ in enumerate(list2_SEQ, start=0):
                self.tableWidget2.setItem(col,4,QTableWidgetItem(SEQ))  
                    
        self.tableWidget1.resizeColumnsToContents()
        self.tableWidget2.resizeColumnsToContents()


    def about(self) :
        QMessageBox.about(self, 
            "About Tag Comparer",
            """<b>Visual Tag Analyzer</b>
               <p>Copyright &copy; 2017 Jeremy Roberts, All Rights Reserved.
               <p>Python %s -- Qt %s -- PyQt %s on %s""" %
            (platform.python_version(),
             QT_VERSION_STR, PYQT_VERSION_STR, platform.system()))

app = QApplication(sys.argv)
widget = MainWindow()
widget.show()
app.exec_()