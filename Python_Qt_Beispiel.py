# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 08:47:42 2023
Dieses Programm ist ein Beispiel für eine Qt Oberfläche für Python Programme
und beinhaltet eine Klasse zum Bilder anzeigen und plotten mittels matplotlib.
@author: Paul Herzler
"""

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox, QDialog
from PyQt5.uic import loadUi
import numpy as np
from PIL import Image


class mainWindow(QMainWindow):
    """Klasse für ein Hauptfenster mit QT """
    
    def __init__(self):
        """Konstruktor für ein Hauptfenster"""
        super().__init__()                                                      # Erbt von QWidget
        loadUi("MainWindow.ui", self)                                           # Oberfläche laden
        self.actionOeffnen.triggered.connect(self.openFile)                     # Funktion dem "Öffnen" Button zuweisen
        self.actionAchsen_anpassen.triggered.connect(self.editPlot)             # Funktion dem "Achsen anpassen" Button zuweisen
        
    def openFile(self):
        """Öffnet eine Datei und lädt das Bild oder Plottet die Werte"""
        dialog_path, selected_filter = QFileDialog.getOpenFileName(self,        # Dialog zum auswählen einer Datei
                                    "Datei laden ...", "",                      # Fenstertitel und vorausgefüllter Dateiname
                                    ("Plotdaten (*.txt);;Bilder (*.png *jpg)")) # Filter für anzuzeigende Dateien
        if dialog_path == "":
            self.statusbar.showMessage("Keine Datei geladen.")                  # Ausgabe in der Statusleiste
            return                                                              # falls keine Datei ausgewählt wurde, beenden
        elif selected_filter == "Plotdaten (*.txt)":
            x, y = np.loadtxt(dialog_path)                                      # lädt die x und y Werte aus einer Textdatei
            self.matplotlibView.plot(x, y)                                      # plottet die Daten mit Hilfe der Methode Plot aus MatplotlibWidgetFile.py
            self.actionAchsen_anpassen.setEnabled(True)                         # macht den "Achsen anpassen" Button anklickbar
        elif selected_filter == "Bilder (*.png *jpg)":
            image = Image.open(dialog_path)                                     # lädt ein Bild
            self.matplotlibView.imshow(np.asarray(image))                       # zeigt das Bild mit Hilfe der Methode imshow aus MatplotlibWidgetFile.py
            self.actionAchsen_anpassen.setEnabled(False)                        # macht den "Achsen anpassen" Button nicht anklickbar
        self.statusbar.showMessage("Datei geladen.")                            # Ausgabe in der Statusleiste
    
    def editPlot(self):
        dialog = dialogWindow("DialogBearbeiten.ui", self)                      # lädt die Dialog UI, als parent wird "self" übergeben, damit wird das Hauptfenster beim Aufruf von exec inaktiv
        if dialog.exec():                                                       # exec zeigt das Dialog Fenster an, gibt 1 zurück wenn accept emittiert wird (Signal des OK Button siehe QTDesigner)
            ax = self.matplotlibView.canvas.fig.axes[0]                         # die matplotlibView ist eine Instanz des MatplotlibWidets
            ax.set_title(dialog.lineEditTitle.text())                           # über canvas.fig können die Achsen des matplotlib verändert werden
            ax.set_xlim(dialog.doubleSpinBoxXlower.value(),
                        dialog.doubleSpinBoxXupper.value())
            ax.set_ylim(dialog.doubleSpinBoxYlower.value(),
                        dialog.doubleSpinBoxYupper.value())
            self.matplotlibView.canvas.draw()                                   # zum schluss muss immer canvas.draw aufgerufen werden, damit das Resultat auch angezeigt wird


class dialogWindow(QDialog):
    """Klasse für ein Dialogfenster mit QT """
    
    def __init__(self, ui, parent=None):
        """Konstruktor für ein Dialogfenster"""    
        super().__init__(parent)                                                # Verknüpfung mit Hauptfenster (Icon wird übernommen)
        loadUi(ui, self)
    


if __name__ == "__main__":                                                      # Hauptprogramm
    app = QApplication(sys.argv)                                                # Applikationsobjekt erzeugen
    ui = mainWindow()                                                           # Instanz anlegen
    ui.show()                                                                   # Widget anzeigen
    QMessageBox.information(ui, "Herzlich Willkommen!",
    "Herzlich Willkommen!\nDieses Programm kann Bilder und Plotdaten anzeigen.")# Willkommensnachricht nach Öffnen des Haupftfensters 
    sys.exit(app.exec_())                                                       # Hauptschleife



