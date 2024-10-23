"""
Definiert die benutzerdefinierte Qt-Klasse matplotlibWidget
Im Qt-Designer wird zunächst ein Widget hinzugefügt.
Anschließend Rechtsklick -> Benutzerdefinierte Klasse
Klassenname: matplotlibWidget
IncludeFile: matplotlibWidgetFile
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
 

class MplCanvas(FigureCanvas):
    """Klasse für eine Canvas Objekt"""
    
    def __init__(self):
        """Konstruktor für ein Canvas Object"""
        self.fig = Figure()                                                     # Figure von matplotlib erstellen
        FigureCanvas.__init__(self, self.fig)                                   # Canvas initialisieren
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
    
 
class matplotlibWidget(QWidget):
    """Klasse für ein matplotlibWidget"""
    
    def __init__(self, parent=None):
        """Konstruktor für ein matplotlibWidget"""
        QWidget.__init__(self, parent)
        self.canvas = MplCanvas()                                               # Canvas zeigt die Plots an
        self.vbl = QVBoxLayout()                                                # Das VBox Layout integriert das ganze in die Qt Oberfläche
        self.vbl.addWidget(self.canvas)                                         # Das Canvas wird den VBox Layout hinzugefügt
        self.setLayout(self.vbl)
    
    def imshow(self, *args):
        """Macht die imshow Funktion aus matplotlib einfacherer erreichbar"""
        self.canvas.fig.clear()
        self.canvas.fig.add_subplot(111)
        self.canvas.fig.axes[0].set_axis_off()
        self.canvas.fig.axes[0].imshow(*args)
        self.canvas.draw()
    
    def plot(self, *args):
        """Macht die plot Funktion aus matplotlib einfacherer erreichbar"""
        self.canvas.fig.clear()
        self.canvas.fig.add_subplot(111)
        self.canvas.fig.axes[0].plot(*args)
        self.canvas.draw()