
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLineEdit, QDialog, 
                             QVBoxLayout, QAction, QMessageBox, QComboBox, 
                             QLabel,QSplitter,QPushButton,QTableWidget,QWidget,
                             QSpacerItem, QInputDialog, QFileDialog, QTableWidgetItem, QCheckBox)
from PyQt5.QtCore import (QT_VERSION_STR, PYQT_VERSION_STR,pyqtSignal)
from PyQt5.QtCore import Qt
from PyQt5.Qt import QGridLayout, QHBoxLayout
from PyQt5 import QtCore, QtGui, QtWidgets
import platform
import sys
import re
#from TagViewer import TagViewer



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
    "combo_box_size": 254,
    "input_size": 99,
    "search_size": 197,
    "query_size": 100
}

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('Visual Tag Analyzer') 

        self.left_tag_viewer = TagViewer()
        self.right_tag_viewer = TagViewer()

        self.loaded_tag_files = {}

        
        # Create the File menu
        self.menuFile = self.menuBar().addMenu("&File")

        self.actionImport = QAction("&Import Genome Tags", self)
        self.actionImport.triggered.connect(self.importgtags)
        """
        self.actionImportroi = QAction("&Import Regions of Interest", self)
        self.actionImportroi.triggered.connect(self.importroi)
        """
        self.actionQuit = QAction("&Quit", self)
        self.actionQuit.triggered.connect(self.close)

        self.menuFile.addActions([self.actionImport,self.actionQuit])
        
        # Create the Help menu
        self.menuHelp = self.menuBar().addMenu("&Help")
        self.actionAbout = QAction("&About",self)
        self.actionAbout.triggered.connect(self.about)
        self.actionUsage = QAction("&Usage",self)
        self.actionUsage.triggered.connect(self.usage)
        self.menuHelp.addActions([self.actionAbout])
        self.menuHelp.addActions([self.actionUsage])
        
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
        self.rangeto1.setFixedWidth(GUI_CONFIG["input_size"]+4)
        self.rangefrom2 = QLineEdit("")
        self.rangefrom2.setFixedWidth(GUI_CONFIG["input_size"])
        self.rangeto2 = QLineEdit("")
        self.rangeto2.setFixedWidth(GUI_CONFIG["input_size"]+4)

        """
        self.roibox = QComboBox()
        self.roibox.addItem("ROI: None")
        self.roibox.setFixedWidth(GUI_CONFIG["combo_box_size"]+5)   

        self.roilabel = QLabel("Restrict tags in ROI:")
        self.roilabel.setBuddy(self.roibox)
        """

        self.searcher = QLineEdit("")
        self.searcher.setFixedWidth(GUI_CONFIG["search_size"])
        
        self.searchlabel = QLabel("Sequence:")
        self.searchlabel.setBuddy(self.searcher)

        self.similarbox = QCheckBox()

        self.similarlabel = QLabel("Compare Similar Seqs:")
        self.similarlabel.setBuddy(self.similarbox)
       
        self.SearchButton = QPushButton("Analyze Query")
        self.SearchButton.setFixedWidth(GUI_CONFIG["query_size"])
        self.SearchButton.setDefault(True)
        self.SearchButton.clicked.connect(self.analyze_query)
        self.SearchButton.clicked.connect(self.highlight)
        
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
        """
        roilayout = QHBoxLayout()
        roilayout.addWidget(self.roilabel)
        roilayout.addWidget(self.roibox)
        roilayout.addStretch(1)
        """
        searchlayout = QHBoxLayout()
        searchlayout.addWidget(self.searchlabel)
        searchlayout.addWidget(self.searcher)
        searchlayout.addSpacerItem(QSpacerItem(12, 0))
        searchlayout.addWidget(self.similarlabel)
        searchlayout.addWidget(self.similarbox)
        searchlayout.addSpacerItem(QSpacerItem(12, 0))
        searchlayout.addWidget(self.SearchButton)
        searchlayout.addStretch(1)  

        
        """
        self.tableWidget1 = QTableWidget(0, 5)
        self.tableWidget2 = QTableWidget(0, 5)
        self.tableWidget1.setHorizontalHeaderLabels((GUI_CONFIG["headerlabels"]).split(";"))
        self.tableWidget2.setHorizontalHeaderLabels((GUI_CONFIG["headerlabels"]).split(";"))
        self.tableWidget1.resizeColumnsToContents()
        self.tableWidget2.resizeColumnsToContents()
        """

        self.viewerlayout = QHBoxLayout()
        self.left_table = self.left_tag_viewer.table_widget
        self.right_table = self.right_tag_viewer.table_widget
        self.viewerlayout.addWidget(self.left_table)
        self.viewerlayout.addWidget(self.right_table)
        self.setLayout(self.viewerlayout)
 

        self.layout = QVBoxLayout()
        self.layout.addLayout(toplayout)
        self.layout.addLayout(midlayout)
        self.layout.addLayout(botlayout)
        self.layout.addSpacerItem(QSpacerItem(0, 12))
        #self.layout.addLayout(roilayout)
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
            if f not in self.loaded_tag_files:
                data = (open(f,"r")).readlines()
                self.loaded_tag_files[f] = list(map(lambda x: self.create_tag(x.split(' ')), data))
                self.genome1.addItem(f)
                self.genome2.addItem(f)

    def create_tag(self, data_line):
        data = Tag()
        data.index = int(data_line[0])
        data.chromosome = data_line[1]
        data.position = int(data_line[2])
        data.quality = data_line[3]
        data.sequence = data_line[4]
        return data



    """
    def importroi(self):   
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Import Genome Tags", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            f= str(fileName)
            if f not in self.loaded_tag_files:
                data = (open(f,"r")).readlines()
                self.loaded_tag_files[f] = list(map(lambda x: x.split(' '), data))
                self.roibox.addItem(f)
    """

    def analyze_query(self):
        self.analyze_side(self.left_tag_viewer, self.rangefrom1.text(), self.rangeto1.text(), self.chromosome1.currentText(), self.genome1.currentText(), self.searcher.text())
        self.analyze_side(self.right_tag_viewer, self.rangefrom2.text(), self.rangeto2.text(), self.chromosome2.currentText(), self.genome2.currentText(), self.searcher.text())
        """
        if (self.similarbox.isChecked()):
            for row in range(self.left_tag_viewer.table_widget.rowCount()):
                for row2 in (self.left_tag_viewer.table_widget.QTableWidgetItem(self, row, 4))

            for = self.left_tag_viewer.table_widget.findItems(QTableWidgetItem(self, 4, QtCore.Qt.MatchExactly)

            for = self.right_tag_viewer.table_widget.findItems(self.edit.text(), QtCore.Qt.MatchExactly)
        """

    
    def highlight(self):
        if self.similarbox.isChecked():
            for ind1,row1 in enumerate(range(self.left_table.rowCount())):
                seq1 = self.left_table.item(row1,4)
                for ind2,row2 in enumerate(range(self.right_table.rowCount())):
                    seq2 = self.right_table.item(row2,4)
                    if str(seq1.text()) == str(seq2.text()):
                        print (str(seq1.text()))
                        print (str(seq2.text()))
                        self.left_table.item(ind1,0).setBackground(QtGui.QColor(112,199,211))
                        self.left_table.item(ind1,1).setBackground(QtGui.QColor(112,199,211))
                        self.left_table.item(ind1,2).setBackground(QtGui.QColor(112,199,211))
                        self.left_table.item(ind1,3).setBackground(QtGui.QColor(112,199,211))
                        self.left_table.item(ind1,4).setBackground(QtGui.QColor(112,199,211))
                        self.right_table.item(ind2,0).setBackground(QtGui.QColor(112,199,211))
                        self.right_table.item(ind2,1).setBackground(QtGui.QColor(112,199,211))
                        self.right_table.item(ind2,2).setBackground(QtGui.QColor(112,199,211))
                        self.right_table.item(ind2,3).setBackground(QtGui.QColor(112,199,211))
                        self.right_table.item(ind2,4).setBackground(QtGui.QColor(112,199,211))

    def analyze_side(self, tag_viewer, range_from_text, range_to_text, chromosome_text, genome_name_text, seq_text):
        data = []
        
        if not re.match(r"Genome [0-9]: None", genome_name_text):
            data = self.loaded_tag_files[genome_name_text]

        if not re.match(r"Chromosome [0-9]: None", chromosome_text):
            tag_viewer.selected_chromosome = chromosome_text
        else:
            tag_viewer.selected_chromosome = None
        
        if range_from_text != "" and range_to_text != "":
            tag_viewer.from_range = int(range_from_text)
            tag_viewer.to_range = int(range_to_text)
        else:
            tag_viewer.from_range = None
            tag_viewer.to_range = None

        if seq_text != "":
            tag_viewer.search_tags = str(seq_text)
        else:
            tag_viewer.search_tags = None

        tag_viewer.load_data(data)



    def about(self) :
        QMessageBox.about(self, 
            "About Tag Comparer",
            "<b>Cameron Amos ME701 Final Project<b>")


    def usage(self):
        QMessageBox.about(self, 
            "Tag Comparer Usage",
            """<p>It is possible to compare two different tags sets from two different genomes at the same time.
            <p> First, Load in a tag file (.txt) using the File -> Import Genome Tags.
            <p> Now it is possible to select that genome from the Genome combo boxes.
            <p> You may query increased specificity on which tags you would like to show up on the screen by choosing what chromosome, base pair range, and specific sequence the tags must have.
            <p> You may also highlight tags that are similar by sequence between the two genomes by checking the 'Compare Similar Seqs' box.
            """)


HEADER_LABELS = ["ID", "CHR", "POS", "Q","SEQ"]

class Tag:
    index = 0
    chromosome = ""
    position = 0
    quality = ""
    sequence = ""

class TagViewer:

    def __init__(self):
        self.table_widget = QTableWidget(0, 5)
        self.table_widget.setHorizontalHeaderLabels(HEADER_LABELS)
        self.table_widget.resizeColumnsToContents()

        self.selected_chromosome = None
        self.from_range = None
        self.to_range = None
        self.search_tags = None
        self.data = []
    
    def load_data(self, data):
        self.data = data
        self.update()



    def update(self):
        if len(self.data) == 0:
            self.table_widget.setRowCount(0)
            return
        
        filtered_data = list(filter(self.is_valid_data, self.data))
        self.table_widget.setRowCount(len(filtered_data))

        for row, data in enumerate(filtered_data):

            self.table_widget.setItem(row, 0, QTableWidgetItem(str(data.index)))
            self.table_widget.setItem(row, 1, QTableWidgetItem(data.chromosome))
            self.table_widget.setItem(row, 2, QTableWidgetItem(str(data.position)))
            self.table_widget.setItem(row, 3, QTableWidgetItem(data.quality))
            self.table_widget.setItem(row, 4, QTableWidgetItem(data.sequence))
        """
            if chromosome in 

        for ind, seq in enumerate(list1_SEQ):
            if str(self.searcher.text()) != '':
                if (str(self.searcher.text())).upper() in list1_SEQ[ind]:
                    for j in range(self.tableWidget1.columnCount()):
                        self.tableWidget1.item(ind,j).setBackground(QtGui.QColor(112,199,211))
        for ind, seq in enumerate(list2_SEQ):
            if str(self.searcher.text()) != '':
                if (str(self.searcher.text())).upper() in list2_SEQ[ind]:
                    for j in range(self.tableWidget2.columnCount()):
                        self.tableWidget2.item(ind,j).setBackground(QtGui.QColor(112,199,211))
        """

        self.table_widget.resizeColumnsToContents()

    def is_valid_data(self, data):
        if self.selected_chromosome and data.chromosome != self.selected_chromosome:
            return False

        if self.from_range and self.to_range:
            if data.position < self.from_range - len(data.sequence) or data.position > self.to_range:
                return False

        if self.search_tags:
                if (self.search_tags).upper() not in data.sequence:
                    return False

        return True



app = QApplication(sys.argv)
widget = MainWindow()
widget.show()
app.exec_()