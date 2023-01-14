import VueDemineur
import Demineur as d
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSignal, Qt
class Controller:
    # ------------------------ Constructeur ------------------------ #
    def __init__(self, screen) -> None:
        self.demineur = d.Demineur(10, 10)
        self.vue = VueDemineur.VueDemineur(screen, self.demineur.getTaille())
        self.vue.updateDemineur(self.demineur)
        # récupère les signaux
        self.vue.boutonNouveauClicked.connect(self.nouvellePartie)
        self.vue.boutonJeuxClicked.connect(self.joue)
    
    # ------------------------ Méthodes ------------------------ #
    
    # permet de relancer une nouvelle partie et de rafraichir la vue 
    def nouvellePartie(self) -> None:
        self.demineur.nouvellePartie()
        self.vue.updateDemineur(self.demineur)
        self.vue.updateCompteur(str(self.demineur.getPerdu), str(self.demineur.getGagne), str(self.demineur.getNbAffichage))
        
    # permet de jouer à l'emplacement souhaiter et de rafraichir la vue 
    def joue(self, position) -> None:
        if (self.demineur.getNbAffichage == 0 and int(position['ligne']+1 != 0 and int(position['col'])+1 != 0)):
            self.demineur.joue(int(position['ligne'])+1, int(position['col'])+1)
        self.vue.updateDemineur(self.demineur)
        self.vue.updateCompteur(self.demineur.getPerdu, self.demineur.getGagne, self.demineur.getNbAffichage)
   
# ------------------------ Main ------------------------ #     
if __name__ == '__main__':
    # create Qt engine
    app = QApplication(sys.argv)
    screeen = app.screens()[0] # selection l'écran ou est l'application
    # cree une application, fenêtre
    win = Controller(screeen)
    sys.exit(app.exec())