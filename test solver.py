from Puzzle_Solver import Solver as solver
from Puzzle_Solver import Bases as bases
from Puzzle_Solver import Piece as piece

class scrollable_canvas () :
    def refresh (self) :
        pass

class canvas () :
    def coutours_pour_bases(self) :
        pass
    def redimentionner (self) :
        pass

class Test () :
    def __init__(self) :
        self.grille_x = 11
        self.grille_y = 5
        self.init_colors()
        self.init_pieces(nb_pieces=len(piece.docu_pieces))
        self.scrollable_canvas = scrollable_canvas()
        self.canvas = canvas()
        self.solver = solver(self)
        self.bases = bases(self)
        self.base_num = 0
        self.bases.ouvrir_base (self.base_num)
        self.creation_pieces = False
        self.grille_resolue = self.solver.resoudre()
        self.affichage()
    
    def affichage (self) :
        x_min = 7
        x_max = 0
        y_min = 0
        y_max = 0
        for ligne in range (y_min,len(self.grille_resolue)-y_max) :
            for el in range (x_min,len(self.grille_resolue[ligne])-x_max) :
                if self.grille_resolue[ligne][el] == "0" :
                    print(self.grille_resolue[ligne][el], end=" | ")
                else :
                    print (self.grille_resolue[ligne][el].nom, end=" | ")
            print()

    def grille_init_dimentions (self) :
        pass

    def init_colors (self) :
        #self.colors = ["blue","green","red","yellow","purple"]
        self.colors = ["#00FFD5","#145E06","#BF1B02","#02DE70",
                       "#FF4AFF","#0515FF","#09016E","#ED0000",
                       "#60D649","#59259C","#FFF566","#FF7700",
                       "#284461","#8A5573","#9F23CC","#7DCC39",
                       "#D4E660","#","#","#",
                       "#","#","#","#",
                       "#","#","#","#"] #couleurs à ajouter
    
    def init_pieces(self,num_piece=0, nb_pieces=1) :
        self.pieces = []
        self.pieces_nom = {}
        for i in range (nb_pieces) :
            p = piece(self, i+num_piece, self.colors[i])
            self.pieces.append(p)
            self.pieces_nom[p.nom] = (p,i)
            p.fin_init()


test = Test()
