from PyQt5.QtWidgets import (QApplication, QMainWindow, QLineEdit, QDialog, 
                             QVBoxLayout, QAction, QMessageBox, QComboBox, QLabel,QSplitter)
from PyQt5.QtCore import (QT_VERSION_STR, PYQT_VERSION_STR,pyqtSignal)
import platform
import sys
from PyQt5.Qt import QGridLayout, QHBoxLayout

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
    "search_size": 289,
}

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('Visual Tag Analyzer') 

        
        # Create the File menu
        self.menuFile = self.menuBar().addMenu("&File")
        self.actionSaveAs = QAction("&Import Genome Tags", self)
        self.actionSaveAs.triggered.connect(self.importgtags)
        self.actionQuit = QAction("&Quit", self)
        self.actionQuit.triggered.connect(self.close)
        self.menuFile.addActions([self.actionSaveAs, self.actionQuit])
        
        # Create the Help menu
        self.menuHelp = self.menuBar().addMenu("&Help")
        self.actionAbout = QAction("&About",self)
        self.actionAbout.triggered.connect(self.about)
        self.menuHelp.addActions([self.actionAbout])
        
        # Setup main widget
        self.setGeometry(300, 300, 250, 150)
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
        
        searchlabel = QLabel("Search tags on screen:")
        searchlabel.setBuddy(self.searcher)
        
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
        searchlayout.addWidget(searchlabel)
        searchlayout.addWidget(self.searcher)
        searchlayout.addStretch(1)  
             
        viewerlayout = QHBoxLayout()



        layout = QVBoxLayout()
        layout.addLayout(toplayout)
        layout.addLayout(midlayout)
        layout.addLayout(botlayout)
        layout.addLayout(searchlayout)

        layout.addLayout(viewerlayout)

        layout.addStretch(1)  
          
        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)
        self.setGeometry(600, 400, 825, 500)

    def importgtags(self) :
        pass
    
    
    
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