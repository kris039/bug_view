# -*- coding: utf-8 -*-
from PyQt5 import QtGui, QtWidgets#,QtCore
import sys, os, re, datetime

class buggy ():
    def __init__(self):
        self.dir = ''

    def callProj(self):
        self.proj = proj()

    def callMainW(self, dir):
        self.window = Window(dir)

    def callRop(self, dir):
        self.dodCli = newRop(dir)

    def callKom(self, pos, dir):
        self.dodKom = newKom(pos, dir)

    def callERop(self, pos, dir):
        self.editCli = editRop(pos, dir)

    def refMain(self):
        self.window.refresh()
# =====================================================================================================================
class proj(QtWidgets.QWidget):
    def __init__(self):
        super(proj, self).__init__()
        self.dir = ''
        self.setObjectName("Proj")
        self.setWindowIcon(QtGui.QIcon('BugView\susp256.ico'))
        self.resize(400, 80)
        self.setWindowTitle("Projekt")
        self.setupProj()

    def setupProj(self):
        vLay = QtWidgets.QGridLayout(self)
        form = QtWidgets.QFormLayout(self)
        form.setSpacing(5)
        self.wyb = QtWidgets.QComboBox(self)
        self.name = QtWidgets.QLineEdit(self)
        self.save = QtWidgets.QPushButton(self)
        l1 = QtWidgets.QLabel(self)
        l2 = QtWidgets.QLabel(self)
        l1.setText('Wybierz folder')
        l2.setText('Stwórz folder')
        self.save.setText('Otwórz folder')
        self.dirList(self.wyb)

        form.addRow(l1, self.wyb)
        form.addRow(l2, self.name)
        vLay.addItem(form)
        vLay.addWidget(self.save)
        self.save.clicked.connect(self.saveDir)
        self.show()

    def none(self):
        box = QtWidgets.QMessageBox.warning(self, 'Message',"Musisz stworzyć nowy folder!")

    def saveDir(self):
        if self.name.text() != '':
            dir = self.name.text() + '_BV'
            self.dir = dir.replace(' ', '_')
            call.callMainW(self.dir)
            self.close()
        elif self.wyb.currentText():
            self.dir = self.wyb.currentText()
            call.callMainW(self.dir)
            self.close()
        else:
            self.none()


    def dirList(self, list):
        for root, dirs, files in os.walk('.'):
            for dir in dirs:
                if re.match('.*_BV$', str(dir)):
                    list.addItem(dir)
        return list
# =====================================================================================================================
class Window(QtWidgets.QWidget):
    def __init__(self, pdir):
        super(Window, self).__init__()
        self.pdir = pdir
        self.setObjectName("BugView")
        self.setWindowIcon(QtGui.QIcon('BugView\susp256.ico'))
        self.resize(700, 600)
        self.mainUi()

    def mainUi(self):
        self.control()
        self.setWindowTitle("BugView")
        self.lPos = ''

        hLay = QtWidgets.QHBoxLayout(self)
        frL = QtWidgets.QFrame(self)
        frR = QtWidgets.QFrame(self)

        self.text = QtWidgets.QTextBrowser()
        self.text.setText('Wybierz raport')

        dodaj = QtWidgets.QPushButton(frR)
        dodaj.setText("Dodaj raport")
        dodaj.clicked.connect(self.dodaj_clicked)

        koment = QtWidgets.QPushButton(frR)
        koment.setText("Dodaj komentarz")
        koment.clicked.connect(self.koment_clicked)

        edit = QtWidgets.QPushButton(frR)
        edit.setText("Edytuj raport")
        edit.clicked.connect(self.edit_clicked)

        refr = QtWidgets.QPushButton(frR)
        refr.setText("Odśwież")
        refr.clicked.connect(self.refresh)

        self.list = QtWidgets.QListWidget(frR)
        self.listFill(self.list)
        self.list.itemClicked.connect(self.textFillEv)

        frR.setMaximumWidth(150)
        hLay.addWidget(frR)
        hLay.addWidget(frL)
        vLayR = QtWidgets.QVBoxLayout(frR)
        vLayR.addWidget(dodaj)
        vLayR.addWidget(koment)
        vLayR.addWidget(edit)
        vLayR.addWidget(refr)
        vLayR.addWidget(self.list)
        vLayL = QtWidgets.QVBoxLayout(frL)
        vLayL.addWidget(self.text)
        self.show()

    def control(self):
        if not os.path.exists(self.pdir):
            dat = datetime.date.today()
            os.makedirs(self.pdir)
            path = os.path.join(self.pdir, 'rop0000.txt')
            file = open(path, 'w')
            file.write(
                '0000~~~~~~~~~~0.0~~~~~~~~~~Kris~~~~~~~~~~' + str(dat) + '~~~~~~~~~~Raport kontrolny~~~~~~~~~~Closed~~~~~~~~~~Zapis niezbędny do rozpoczęcia pracy z programem')
            file.close()

    def listPos(self, lis, arg):                         # 1 - zapis, 2 - odczyt
        if arg == 1:
            self.lPos = lis
        else:
            return lis

    def dodaj_clicked(self):
        call.callRop(self.pdir)

    def koment_clicked(self):
        if len(self.lPos) <= 4:
            self.nonC()
        else:
            call.callKom(self.lPos, self.pdir)

    def edit_clicked(self):
        if len(self.lPos) <= 4:
            self.nonCE()
        else:
            call.callERop(self.lPos, self.pdir)

    def textFillEv(self, value):
        name = value.text()
        path = os.path.join(self.pdir, name)
        t = open(path, 'r')
        text = t.read()
        t.close()
        text = text.replace('~'*10,'\n',5)
        text = text.replace('~'*10,'\n\n')
        self.text.setText(text)
        self.listPos(name, 1)


    def refresh(self):
        self.list.clear()
        self.listFill(self.list)
        if len(self.lPos) > 4:
            path = os.path.join(self.pdir, self.lPos)
            t = open(path, 'r')
            text = t.read()
            t.close()
            text = text.replace('~' * 10, '\n', 5)
            text = text.replace('~' * 10, '\n\n')
            self.text.setText(text)

    def listFill(self, list):
        for root, dirs, files in os.walk(self.pdir):
            for file in files:
                if re.match(r'^rop[0-9]+', file):
                    list.addItem(file)
        return list

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Message',
                                               "Na pewno?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def nonC(self):
        box = QtWidgets.QMessageBox.warning(self, 'Message',"Wybierz raport do skomentowania")

    def nonCE(self):
        box = QtWidgets.QMessageBox.warning(self, 'Message',"Wybierz raport do edycji")
# =====================================================================================================================
class newRop(QtWidgets.QWidget):
    def __init__(self, pdir):
        super(newRop, self).__init__()
        self.pdir = pdir
        self.setObjectName("NewRop")
        self.setWindowIcon(QtGui.QIcon('BugView\susp256.ico'))
        self.resize(500, 400)
        self.setWindowTitle("Nowy raport")
        self.setupRop()

    def setupRop(self):
        vLay = QtWidgets.QGridLayout(self)
        form = QtWidgets.QFormLayout(self)
        form.setSpacing(5)
        self.nr = QtWidgets.QLineEdit(self)
        valid = QtGui.QIntValidator()
        self.nr.setValidator(valid)
        self.nr.setMaxLength(4)
        self.rea = QtWidgets.QLineEdit(self)
        self.who = QtWidgets.QLineEdit(self)

        frLay = QtWidgets.QHBoxLayout(self)
        self.date = QtWidgets.QLineEdit(self)
        self.dateB = QtWidgets.QPushButton(self)
        self.dateB.setText('Dzisiaj')
        frLay.addWidget(self.date)
        frLay.addWidget(self.dateB)
        self.sub = QtWidgets.QLineEdit(self)
        self.sta = QtWidgets.QComboBox(self)
        self.fillCom(self.sta)
        self.des = QtWidgets.QTextEdit(self)
        self.save = QtWidgets.QPushButton(self)
        self.save.setText('Zapisz nowy raport')
        l1 = QtWidgets.QLabel(self)
        l2 = QtWidgets.QLabel(self)
        l3 = QtWidgets.QLabel(self)
        l4 = QtWidgets.QLabel(self)
        l5 = QtWidgets.QLabel(self)
        l6 = QtWidgets.QLabel(self)

        l1.setText('Numer raportu')
        l2.setText('Realease')
        l3.setText('Kto dodaje')
        l4.setText('Data')
        l5.setText('Temat')
        l6.setText('Stan')

        form.addRow(l1, self.nr)
        form.addRow(l2, self.rea)
        form.addRow(l3, self.who)
        form.addRow(l4, frLay)
        form.addRow(l5, self.sub)
        form.addRow(l6, self.sta)

        self.nr.setText(self.newNum())

        vLay.addItem(form)
        vLay.addWidget(self.des)
        vLay.addWidget(self.save)

        # self.ref = ui.refresh
        self.save.clicked.connect(self.clickedSave)
        self.dateB.clicked.connect(self.dateFill)
        self.show()

    def dateFill(self):
        date = str(datetime.date.today())
        self.date.setText(date)

    def newNum(self):
        a = max(self.listKeys())
        a += 1
        return str(a)

    def ropNum(self):
        return self.nr.text()
    def ropVer(self):
        return self.rea.text()
    def ropWho(self):
        return self.who.text()
    def ropDate(self):
        return self.date.text()
    def ropSub(self):
        return self.sub.text()
    def ropState(self):
        return self.sta.currentText()
    def ropDesc(self):
        return self.des.toPlainText()

    def clickedSave(self):
        num = self.ropNum()
        if num == '':
            self.zero()
        elif self.checkKey(num):
            self.occu()
        elif self.dial():
            text = self.getRop()
            name = 'rop'+num.zfill(4)+'.txt'
            path = os.path.join(self.pdir, name)
            t = open(path, 'w')
            t.write(text)
            call.refMain()
            t.close()

            self.close()
        else:
            pass

    def getRop(self):
        text = ''
        sep = '~'*10
        text += self.ropNum() + sep
        text += self.ropVer() + sep
        text += self.ropWho() + sep
        text += self.ropDate() + sep
        text += self.ropSub() + sep
        text += self.ropState() + sep
        text += self.ropDesc()
        return text

    def checkKey(self,key):
        if int(key) in self.listKeys():
            return True
        else:
            return False

    def listKeys(self):
        keys = []
        list = []
        self.listFill(list)
        for file in list:
            key = int(file[3:7])
            keys.append(key)
        return keys

    def fillCom(self, com):
        com.addItem('New')
        com.addItem('Correction')
        com.addItem('Corrected')
        com.addItem('Verified')
        com.addItem('CorrectionNeeded')
        com.addItem('Closed')

    def listFill(self, list):
        for root, dirs, files in os.walk(self.pdir):
            for file in files:
                if re.match(r'^rop[0-9]+', file):
                    list.append(file)
        return list

    def dial(self):
        reply = QtWidgets.QMessageBox.question(self, 'Message',
             "Na pewno?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            return True
        else:
            return False

    def occu(self):
        box = QtWidgets.QMessageBox.warning(self, 'Message',"Numer zajęty")

    def zero(self):
        box = QtWidgets.QMessageBox.warning(self, 'Message',"Wpisz wartość")
# =====================================================================================================================
class newKom(QtWidgets.QWidget):
    def __init__(self, pos, pdir):
        super(newKom, self).__init__()
        self.pos = pos
        self.pdir = pdir
        self.setObjectName("NewKom")
        self.setWindowIcon(QtGui.QIcon('BugView\susp256.ico'))
        self.resize(400, 200)
        self.setWindowTitle("Nowy komentarz")
        self.setupKom()

    def setupKom(self):
        vLay = QtWidgets.QGridLayout(self)
        form = QtWidgets.QFormLayout(self)
        form.setSpacing(5)
        self.who = QtWidgets.QLineEdit(self)
        frLay = QtWidgets.QHBoxLayout(self)
        self.date = QtWidgets.QLineEdit(self)
        self.dateB = QtWidgets.QPushButton(self)
        self.dateB.setText('Dzisiaj')
        frLay.addWidget(self.date)
        frLay.addWidget(self.dateB)

        self.des = QtWidgets.QTextEdit(self)
        self.save = QtWidgets.QPushButton(self)
        self.save.setText('Zapisz nowy komentarz')
        self.save.clicked.connect(self.saveKom)
        self.dateB.clicked.connect(self.dateFill)

        l1 = QtWidgets.QLabel(self)
        l2 = QtWidgets.QLabel(self)

        l1.setText('Kto dodaje')
        l2.setText('Data')

        form.addRow(l1, self.who)
        form.addRow(l2, frLay)
        vLay.addItem(form)
        vLay.addWidget(self.des)
        vLay.addWidget(self.save)
        self.show()

    def dateFill(self):
        date = str(datetime.date.today())
        self.date.setText(date)

    def saveKom(self):
        if self.dial():
            text = self.getKom()
            name = self.pos
            path = os.path.join(self.pdir, name)
            t = open(path, 'a')
            t.write(text)
            t.close()
            call.refMain()
            self.close()
        else:
            pass

    def komDate(self):
        return self.who.text()

    def komWho(self):
        return self.date.text()

    def komDesc(self):
        return self.des.toPlainText()

    def getKom(self):
        text = '\n'+'-'*50+'\n'
        text += self.komDate() + '\n'
        text += self.komWho() + '\n\n'
        text += self.komDesc()
        return text

    def dial(self):
        reply = QtWidgets.QMessageBox.question(self, 'Message',
             "Na pewno?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            return True
        else:
            return False
# =====================================================================================================================
class editRop(QtWidgets.QWidget):
    def __init__(self, pos, pdir):
        super(editRop, self).__init__()
        self.pos = pos
        self.pdir = pdir
        self.setObjectName("EditRop")
        self.setWindowIcon(QtGui.QIcon('BugView\susp256.ico'))
        self.resize(500, 400)
        self.setWindowTitle("Edytuj raport")
        self.setupERop()

    def setupERop(self):
        vLay = QtWidgets.QGridLayout(self)
        form = QtWidgets.QFormLayout(self)
        form.setSpacing(5)
        self.nr = QtWidgets.QLineEdit(self)
        self.nr.setReadOnly(True)
        self.rea = QtWidgets.QLineEdit(self)
        self.who = QtWidgets.QLineEdit(self)
        self.date = QtWidgets.QLineEdit(self)
        self.sub = QtWidgets.QLineEdit(self)
        self.sta = QtWidgets.QComboBox(self)
        self.fillCom(self.sta)
        self.des = QtWidgets.QTextEdit(self)
        self.save = QtWidgets.QPushButton(self)
        self.save.setText('Zapisz raport')
        l1 = QtWidgets.QLabel(self)
        l2 = QtWidgets.QLabel(self)
        l3 = QtWidgets.QLabel(self)
        l4 = QtWidgets.QLabel(self)
        l5 = QtWidgets.QLabel(self)
        l6 = QtWidgets.QLabel(self)

        l1.setText('Numer raportu')
        l2.setText('Realease')
        l3.setText('Kto dodaje')
        l4.setText('Data')
        l5.setText('Temat')
        l6.setText('Stan')

        form.addRow(l1, self.nr)
        form.addRow(l2, self.rea)
        form.addRow(l3, self.who)
        form.addRow(l4, self.date)
        form.addRow(l5, self.sub)
        form.addRow(l6, self.sta)
        vLay.addItem(form)
        vLay.addWidget(self.des)
        vLay.addWidget(self.save)

        self.show()
        self.setValues()

        self.save.clicked.connect(self.clickedSave)

    def setValues(self):
        name = self.pos
        path = os.path.join(self.pdir, name)
        t = open(path, 'r')
        text = t.read()
        t.close()
        text = text.split('~'*10)
        self.nr.setText(text[0])
        self.rea.setText(text[1])
        self.who.setText(text[2])
        self.date.setText(text[3])
        self.sub.setText(text[4])
        sta = text[5]
        self.des.setText(text[6])
        self.setState(sta)

    def setState(self, sta):
        self.sta.setCurrentText(sta.rstrip())

    def ropNum(self):
        return self.nr.text()
    def ropVer(self):
        return self.rea.text()
    def ropWho(self):
        return self.who.text()
    def ropDate(self):
        return self.date.text()
    def ropSub(self):
        return self.sub.text()
    def ropState(self):
        return self.sta.currentText()
    def ropDesc(self):
        return self.des.toPlainText()

    def clickedSave(self):
        text = self.getRop()
        name = self.pos
        path = os.path.join(self.pdir, name)
        t = open(path, 'w')
        t.write(text)
        t.close()
        call.refMain()
        self.close()

    def getRop(self):
        text = ''
        sep = '~'*10
        text += self.ropNum() + sep
        text += self.ropVer() + sep
        text += self.ropWho() + sep
        text += self.ropDate() + sep
        text += self.ropSub() + sep
        text += self.ropState() + sep
        text += self.ropDesc()
        return text

    def checkKey(self,key):
        if int(key) in self.listKeys():
            return True
        else:
            return False

    def listKeys(self):
        keys = []
        list = []
        self.listFill(list)
        for file in list:
            key = int(file[3:7])
            keys.append(key)
        return keys

    def fillCom(self, com):
        com.insertItem(1, 'New')
        com.insertItem(2, 'Correction')
        com.insertItem(3, 'Corrected')
        com.insertItem(4, 'Verified')
        com.insertItem(5, 'CorrectionNeeded')
        com.insertItem(6, 'Closed')

    def listFill(self, list):
        for root, dirs, files in os.walk("."):
            for file in files:
                if re.match(r'^rop[0-9]+', file):
                    list.append(file)
        return list

    def dial(self):
        reply = QtWidgets.QMessageBox.question(self, 'Message',
             "Na pewno?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            return True
        else:
            return False

    def occu(self):
        box = QtWidgets.QMessageBox.warning(self, 'Message',"Numer zajety")

    def zero(self):
        box = QtWidgets.QMessageBox.warning(self, 'Message',"Wpisz wartosc")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    call = buggy()
    call.callProj()
    sys.exit(app.exec_())

