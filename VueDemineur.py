import sys
import Demineur as d
from PyQt6.QtWidgets import QWidget, QApplication, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtGui import QScreen
from PyQt6.QtCore import pyqtSignal, Qt

class VueDemineur(QWidget):
    # ------------------------ Signaux ------------------------ #
    
    boutonJeuxClicked : pyqtSignal = pyqtSignal(dict)
    boutonNouveauClicked : pyqtSignal = pyqtSignal()
    
    # ------------------------ Constructeur ------------------------ #
    
    def __init__(self, screeen : QScreen, taille : int) -> None:
        super().__init__()
        self.setWindowTitle("Demineur CZARKOWSKI Matthieu")
        self.listebouton = []
        self.taille : int = taille;
        widthS= screeen.size().width()
        heightS = screeen.size().height()
        self.move(widthS//2-400, heightS//2-300)
        self.resize(400, 600)
        
        # layout principal vertical
        self.mainLayout : QVBoxLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        
        # ajoute au layout pricipal le widget du jeu et le widget top
        self.mainWidget : QWidget = QWidget()
        self.mainWidgetTop : QWidget = QWidget()
        self.mainLayout.addWidget(self.mainWidgetTop)
        self.mainLayout.addWidget(self.mainWidget)
        self.mainWidgetTop.setMaximumHeight(30)
        self.mainWidgetTop.setMaximumWidth(3000)
        
        # layout top et ajout du layout au top widget
        self.topLayout : QHBoxLayout = QHBoxLayout()
        self.mainWidgetTop.setLayout(self.topLayout)
        
        # ajout widget contenu dans le widget top
        self.compteurPerdu : QLabel = QLabel("nombre(s) de partie(s) perdue(s) : 0")
        self.topLayout.addWidget(self.compteurPerdu)
        self.compteurPerdu.setFixedSize(200, 20)
        self.message : QLabel = QLabel(" ")
        self.topLayout.addWidget(self.message)
        self.message.setFixedSize(100, 20)
        self.compteurGagne : QLabel = QLabel("nombre(s) de partie(s) gagnée(s) : 0")
        self.topLayout.addWidget(self.compteurGagne)
        self.compteurGagne.setFixedSize(200,20)

        # layout main pour le demineur et ajout du GridLayout layout au main widget
        self.grille_layout = QGridLayout()
        self.mainWidget.setLayout(self.grille_layout)
        self.placeBouton()
        
        # ajout d'un en bas du main layout
        self.nouvelle : QPushButton = QPushButton("nouvelle partie")
        self.mainLayout.addWidget(self.nouvelle)
        
        # signal
        self.nouvelle.clicked.connect(lambda:self.nouvellePartie())

        # affichage
        self.show()
        
    # ------------------------ Méthodes ------------------------ #
    
    # permet de placer les boutons dans la grid et de leur donner un signal quand ils sont cliquées avec leur position pour permettre de joué
    def placeBouton(self):
        for i in range(0, self.taille):
            for y in range(0, self.taille):
                self.bouton : QPushButton = QPushButton(" ")
                self.bouton.clicked.connect(lambda state, i2=i, y2=y : self.joue(i2, y2, state))
                self.listebouton.append(self.bouton)
                self.grille_layout.addWidget(self.bouton, i, y)
                
    # permet de joué en fonction de la position ligne colonne passé en paramètre représentant ou ce situe le bouton et d'émettre un signal avec les positions quand il est cliqué           
    def joue(self, ligne, col , t):  
        if(t != "nouvellepartie"):
            position : dict = {'ligne':ligne, 'col':col}
            self.boutonJeuxClicked.emit(position)
    
    # permet de relance une nouvelle partie et d'émettre un signal quand le bouton est cliqué     
    def nouvellePartie(self):
        self.boutonNouveauClicked.emit()
        self.joue(0, 0, "nouvellepartie")
        self.message.setText("")
    
    # permet de mettre a jour les compteurs de win et loose et d'indiquer si on a perdu ou non
    def updateCompteur(self, comptePerdu, compteGagne, nbMessage):
        self.compteurPerdu.setText("nombre(s) de partie(s) perdue(s) : " + str(comptePerdu))
        self.compteurGagne.setText("nombre(s) de partie(s) gagnée(s) : " + str(compteGagne))
        if nbMessage == 1:
            self.message.setText("Vous avez perdu !")
        elif nbMessage == 2:
            self.message.setText("Vous avez gagné !")
        else:
            self.message.setText("")
    
    # permet de mettre a jour le contenu des boutons et de la grille
    def updateDemineur(self, demineur):
        v = 0
        for i in range(0, self.taille):
            for y in range(0, self.taille):
                self.listebouton[v].setText(str(demineur.getCase(i, y)))
                v += 1
                