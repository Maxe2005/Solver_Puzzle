# Créé le 27/05/22
# Dernière modification : 29/08/23
# Auteur : Maxence CHOISEL

from tkinter import*
from tkinter.messagebox import*
from tkinter.simpledialog import*#askinteger, askstring
from math import log, cos, sin, radians, sqrt
from functools import partial
from random import randint
from csv import writer


class Fenetre (Tk) :
    def __init__(self,x=1300, y=800) :
        Tk.__init__(self)
        self.x = x
        self.y = y
        self.title("Solver de Puzzles")
        self.geometry (str(x)+"x"+str(y))
        self.min_x , self.min_y = 500,400
        self.minsize(self.min_x, self.min_y)
        
        self.proportion_canvas_x = 8/10
        self.proportion_canvas_y = 3/4
        self.grid_columnconfigure(0, weight= 8, minsize= self.proportion_canvas_x*self.min_x)
        self.grid_columnconfigure(1, weight= 2, minsize= (1-self.proportion_canvas_x)*self.min_x)
        self.grid_rowconfigure(0, weight= 1, minsize= (1-self.proportion_canvas_y)*self.min_y)
        self.grid_rowconfigure(1, weight= 3, minsize= self.proportion_canvas_y*self.min_y)
        self.init_grille ()
        self.solver = Solver(self)
        self.bind("<Button-3>", self.redimentionner)
        self.init_colors()
        self.init_pieces(nb_pieces=len(Piece.docu_pieces))
        
        
        self.canvas = Affiche(self,
                              self.proportion_canvas_x*self.x,
                              self.proportion_canvas_y*self.y)
        self.canvas.grid(row=1, column=0, sticky=NSEW)
        
        self.bases = Bases(self)
        
        self.boutons = Boutons(self)
        self.boutons.grid(row=0, column= 1, rowspan=2, sticky=NSEW)
        
        self.creation_pieces = False
        
        self.scrollable_canvas = ScrollableCanvas(self,
                                                  self.proportion_canvas_x*self.x,
                                                  (1-self.proportion_canvas_y)*self.y)
        self.scrollable_canvas.grid(row=0, column=0, sticky=NSEW)
        
        self.canvas.fin_init()
        
        #"""
        self.inser_piece((0,0),num_piece=1)
        self.inser_piece((9,2),num_piece=0)
        #"""
        self.scrollable_canvas.refresh()
        self.canvas.refresh()
        
    def extraction_grille_piece (self) :
        x_min = self.grille_x-1
        y_min = self.grille_y-1
        x_max = y_max = 0
        for j in range (self.grille_y) :
            for i in range (self.grille_x) :
                if self.grille[j][i] != "0" :
                    if i < x_min :
                        x_min = i
                    if i > x_max :
                        x_max = i
                    if j < y_min :
                        y_min = j
                    if j > y_max :
                        y_max = j
        assert x_min < x_max and y_min < y_max
        l = ["0"]*(x_max-x_min+1)
        g = []
        for i in range (y_max-y_min+1) :
            g.append(l.copy())
        for j in range (len(g)) :
            for i in range (len(l)) :
                if self.grille[y_min+j][x_min+i] != "0" :
                    g[j][i] = "1"
        return g
        
    def save_as (self,doc, nom_objet, grille) :
        nom = doc+"/"+nom_objet
        with open (nom, "w", newline = "") as f :
            ecrire = writer (f, delimiter = ",", lineterminator = "\n")
            for i in range (len(grille)) :
                ecrire.writerow (grille[i])
                    
    def enregistrer_piece(self) :
        MsgBox = askquestion ('Enregistrer une piece','Voulez-vous vraiment enregistrer la piece actuellement représentée dans la grille ?',icon = 'warning')
        if MsgBox == 'yes':
            nom = askstring ( title = "Nom de la piece"  , prompt = "Quel sera le nom de la piece à enregistrer ?" , initialvalue = "")
            if nom == None :
                showinfo ('Erreur','L´enregistrement à échoué car aucun nom n´a été saisi !',icon = 'error')
                return
            else :
                grille = self.extraction_grille_piece()
                self.save_as ("Pieces",nom, grille)
                fichier_docu_pieces = open("Pieces/#docu pieces","a")
                fichier_docu_pieces.write(nom+"\n")
                fichier_docu_pieces.close()
                a = ouvrir_docu_pieces()
                self.ajoute_piece(num_piece=len(a)-1, source=a)
                self.scrollable_canvas.refresh()
                showinfo ('Piece enregistré','La piece "'+nom+'" à bien été enregisté !\n Elle est maintenant disponible dans le menu déroulant des pieces')

    def creer_piece (self) :
        self.bases.desactiver()
        if self.boutons.text_creer_piece.get() == "Créer Piece":
            self.boutons.afficher_enregistrer()
            self.creation_pieces = True
            self.init_grille ()
            self.canvas.refresh()
            showinfo ('Créer une nouvelle piece','Pour créer votre piece cliquez sur les cases qui la composent puis enregistrez.')
            self.boutons.text_creer_piece.set("Créer Piece:\nArrêter")
        else :
            self.boutons.cacher_enregistrer()
            self.creation_pieces = False
            self.init_grille ()
            self.canvas.refresh()
            self.boutons.text_creer_piece.set("Créer Piece")
      
    def redimentionner (self,event=None) :
        self.x = self.winfo_width()
        self.y = self.winfo_height()
        self.boutons.redimentionner()
        self.canvas.redimentionner()
        self.scrollable_canvas.redimentionner()
    
    def init_grille (self,x=11, y=5) :
        self.grille = []
        ligne = ["0"]*x
        for i in range (y) :
            self.grille.append(ligne.copy())
        self.grille_init_dimentions()
     
    def grille_init_dimentions (self) :
        self.grille_x = len(self.grille[0])
        self.grille_y = len(self.grille)
             
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
        assert nb_pieces <= len(self.colors)
        self.pieces = []
        self.pieces_nom = {}
        for i in range (nb_pieces) :
            p = Piece(self, i+num_piece, self.colors[i])
            self.pieces.append(p)
            self.pieces_nom[p.nom] = (p,i)
            p.fin_init()
             
    def ajoute_piece (self,num_piece=0, source=None) :
        p = Piece(self, num_piece, self.colors[len(self.pieces)], source)
        self.pieces.append(p)
        self.scrollable_canvas.pieces_affichees.append(p)

    def inser_piece (self, pos, piece=0, num_piece=0) :
        if not(piece) :
            piece = self.pieces[num_piece]
        for j in range (piece.y) :
            for i in range (piece.x) :
                if piece.grille[j][i] == "1" :
                    self.grille[pos[1]+j][pos[0]+i] = piece
        self.scrollable_canvas.pieces_affichees[piece.num] = None
        self.scrollable_canvas.refresh()

    def change_taille_grille(self) :
        n = askstring ( title = "Nouvelles dimentions de grille"  , prompt = "Entrer le nombre de cases en largeur et en hauteur sous la forme : 'largeur,hauteur'" , initialvalue = "x,y")
        if n != None :
            try :
                a = n.split(",")
                x , y = int(a[0]), int(a[1])
            except :
                showinfo ('Erreur','Oups.... Il y a eu une erreur de saisie !',icon = 'error')
                return
            else :
                if 2 < x < 30 and 2 < y < 30 :
                    self.bases.desactiver()
                    self.init_grille (x,y)
                    self.canvas.redimentionner()
                else :
                    showinfo ('Erreur','Oups.... Il y a eu une erreur de saisie :\nLes valeurs doivent être comprisent entre 3 et 29 !',icon = 'error')

    def retirer_piece (self, piece) :
        for j in range (self.grille_y) :
            for i in range (self.grille_x) :
                if self.grille[j][i] == piece :
                    self.grille[j][i] = "0"
        self.scrollable_canvas.pieces_affichees[piece.num] = piece
        self.scrollable_canvas.refresh()
    

class Bases () :
    def __init__(self, boss=None) :
        self.boss = boss
        self.docu_bases = self.ouvrir_doc("#docu bases")
        self.bases_on = False
        self.base_num = 0
        self.base = None
        self.nom = ""

    def ouvrir_doc (self, nom_doc) :
        nom = "Bases/"+nom_doc
        fichier = open (nom, "r")
        table = []
        for ligne in fichier :
            ligne = ligne.rstrip()
            if "," in ligne :
                ligne = ligne.split(",")
            table.append(ligne)
        fichier.close()
        return table

    def transformation_grille_out (self) :
        g = []
        f = self.boss.scrollable_canvas.pieces_affichees.copy()
        e = self.boss.grille.copy()
        e[0:0] = [f]
        for ligne in e :
            a = []
            for el in ligne :
                if el == "0" or el == None :
                    a.append(el)
                else :
                    a.append(el.nom)
            g.append(a)
        return g
    
    def transformation_grille_in (self,grille) :
        g = []
        for ligne in grille :
            a = []
            for el in ligne :
                if el == "0" :
                    a.append(el)
                else :
                    a.append(self.boss.pieces_nom[el][0])
            g.append(a)
        return g
     
    def enregistrer_comme_base (self) :
        if self.boss.creation_pieces :
            showinfo ('Erreur','La fonction "Enregistrer comme une base" n´est pas disponible car le mode "Création de pieces" est activé !',icon = 'error')
        elif self.base == self.boss.grille :
            showinfo ('Erreur','Cette base existe déjà !',icon = 'error')
        else :
            MsgBox = askquestion ('Enregistrer une configuration de départ',
                                             'Voulez-vous vraiment enregistrer la configuration de pieces actuellement représentée dans la grille ?',icon = 'warning')
            if MsgBox == 'yes':
                nom = askstring ( title = "Nom de la configuration"  , prompt = "Quel sera le nom de la configuration à enregistrer ?" , initialvalue = "")
                if nom == None :
                    showinfo ('Erreur','L´enregistrement à échoué car aucun nom n´a été saisi !',icon = 'error')
                    return
                else :
                    grille = self.transformation_grille_out()
                    self.boss.save_as ("Bases",nom, grille)
                    fichier_docu_pieces = open("Bases/#docu bases","a")
                    fichier_docu_pieces.write(nom+"\n")
                    fichier_docu_pieces.close()
                    self.docu_bases.append(nom)
                    showinfo ('Configuration enregistré','La configuration de base "'+nom+'" à bien été enregisté !\n Elle est maintenant disponible dans le bouton Bases')
  
    def ouvrir_base (self,num) :
        self.nom = self.docu_bases[num]
        grille = self.ouvrir_doc(self.nom)
        a = []
        for el in grille.pop(0) :
            if el == "" :
                a.append(None)
            else :
                a.append(self.boss.pieces_nom[el][0])
        self.boss.scrollable_canvas.pieces_affichees = a
        g = self.transformation_grille_in (grille)
        self.boss.grille = g.copy()
        self.base = g.copy()
        self.boss.grille_init_dimentions()
        self.boss.canvas.redimentionner()
        self.boss.canvas.coutours_pour_bases()
        self.boss.scrollable_canvas.refresh()
        
    def bases_on_off (self) :
        if self.boss.creation_pieces :
            showinfo ('Erreur','La fonction "Bases" n´est pas disponible car le mode "Création de pieces" est activé !',icon = 'error')
        else :
            if self.bases_on :
                self.desactiver()
                self.boss.canvas.effacer_grille()
            else :
                self.bases_on = True
                self.ouvrir_base (self.base_num)
    
    def bases_plus(self) :
        if self.boss.creation_pieces :
            showinfo ('Erreur','La fonction "Passer à la base suivante" n´est pas disponible car le mode "Création de pieces" est activé !',icon = 'error')
        else :
            if self.bases_on :
                if self.base_num == len(self.docu_bases)-1 :
                    showinfo ('Erreur','Vous êtes déjà sur la dernière base !',icon = 'error')
                else :
                    self.base_num += 1
                    self.ouvrir_base (self.base_num)
            else :
                self.bases_on_off()
    
    def bases_moins(self) :
        if self.boss.creation_pieces :
            showinfo ('Erreur','La fonction "Aller à la base précédente" n´est pas disponible car le mode "Création de pieces" est activé !',icon = 'error')
        else :
            if self.bases_on :
                if self.base_num == 0 :
                    showinfo ('Erreur','Vous êtes déjà sur la première base !',icon = 'error')
                else :
                    self.base_num -= 1
                    self.ouvrir_base (self.base_num)
            else :
                self.bases_on_off()

    def desactiver (self) :
        self.bases_on = False
        self.base = None
        self.nom = ""
        self.boss.canvas.coutours_pour_bases()














class Affiche (Canvas) :
    def __init__(self, boss=None, x=900, y=700) :
        Canvas.__init__(self,boss)
        self.boss = boss
        self.x = x
        self.y = y
        self.taille_auto ()
        self.origines ()
        self.type_affichage = "carre"
        self.deplace_body_piece = False
        self.piece_en_dep = 0
        self.bind("<Double-Button-1>",self.double_clic)
        self.bind("<Button-1>", self.clic)
        self.bind("<Button1-Motion>", self.mouseMove)
        self.bind("<Button1-ButtonRelease>", self.mouseUp)
        self.boss.bind("<Up>", self.fleche_haut)
        self.boss.bind("<Down>", self.fleche_bas)
        self.boss.bind("<Right>", self.fleche_droite)
        self.boss.bind("<Left>", self.fleche_gauche)
        
        
    def fin_init (self) :
        self.couleur_mode = "black" #l´inverse de la couleur voulue au départ
        self.couleurs ()
        self.configure(width=self.x, height=self.y, bg=self.color)


    def taille_auto (self) :
        "Calcule la taille en pixel d´un coté des cases carré à partir de la hauteur h et le la longeur l de la grille de définition"
        if self.y / self.boss.grille_y < self.x / self.boss.grille_x :
            self.taille = self.y / (self.boss.grille_y+2)
        else :
            self.taille = self.x / (self.boss.grille_x+2)
        self.taille_contours_grille = self.taille/15
        self.taille_lignes_grille = self.taille/15
        self.bordure_ronds = 1/10*self.taille


    def origines (self) :
        "Calcule et renvoi sous forme de tuple les origines en x et y (en haut à gauche du canvas)"
        self.origine_x = (self.x - (self.taille * (self.boss.grille_x))) / 2
        self.origine_y = (self.y - (self.taille * (self.boss.grille_y))) / 2
        assert self.origine_x > 0 and self.origine_y > 0


    def trace_grille (self) :
        "Trace avec Tkinter un quadrillage de la grille g"
        nb_cases_vides = 0
        if self.type_affichage == "carre" :
            self.create_rectangle (self.origine_x, self.origine_y,
                                   self.origine_x+self.taille*(self.boss.grille_x),
                                   self.origine_y+self.taille*(self.boss.grille_y),
                                   fill= self.color)
            for i in range (self.boss.grille_y-1) :
                self.barre_horizontale (self.origine_x, self.origine_y + self.taille * (i+1),
                                        self.taille * self.boss.grille_x,
                                        self.color_grille, self.taille_lignes_grille)
            for i in range (self.boss.grille_x-1) :
                self.barre_verticale (self.origine_x + self.taille * (i+1), self.origine_y,
                                        self.taille * self.boss.grille_y,
                                        self.color_grille, self.taille_lignes_grille)
        elif self.type_affichage == "rond" :
            self.create_rectangle (self.origine_x, self.origine_y,
                                   self.origine_x+self.taille*(self.boss.grille_x),
                                   self.origine_y+self.taille*(self.boss.grille_y),
                                   fill= self.color_grille)
                        
        for j in range (self.boss.grille_y) :
            for i in range (self.boss.grille_x) :
                piece = self.boss.grille[j][i]
                if self.type_affichage == "rond" :
                    add = self.bordure_ronds
                else :
                    add = 0
                depart_x = self.origine_x + self.taille * i + add
                depart_y = self.origine_y + self.taille * j + add
                if piece != "0" :
                    if self.type_affichage == "carre" :
                        self.create_rectangle (depart_x, depart_y,
                                   depart_x + self.taille, depart_y + self.taille ,
                                   fill= piece.color)
                    elif self.type_affichage == "rond" :
                        if i < self.boss.grille_x-1 and \
                           self.boss.grille[j][i+1] != "0" and \
                           self.boss.grille[j][i+1] == piece :
                            depart_x2 = depart_x+(self.taille-2*self.bordure_ronds)/2
                            depart_y2 = depart_y+(self.taille-2*self.bordure_ronds)*3/10
                            self.create_rectangle (depart_x2, depart_y2,
                                                   depart_x2 + (self.taille-2*self.bordure_ronds),
                                                   depart_y2 + (self.taille-2*self.bordure_ronds)*4/10 ,
                                                   fill= piece.color, outline=piece.color)
                        if j < self.boss.grille_y-1 and \
                           self.boss.grille[j+1][i] != "0" and \
                           self.boss.grille[j+1][i] == piece :
                            depart_x2 = depart_x+(self.taille-2*self.bordure_ronds)*3/10
                            depart_y2 = depart_y+(self.taille-2*self.bordure_ronds)/2
                            self.create_rectangle (depart_x2, depart_y2,
                                                   depart_x2 + (self.taille-2*self.bordure_ronds)*4/10,
                                                   depart_y2 + (self.taille-2*self.bordure_ronds) ,
                                                   fill= piece.color, outline=piece.color)
                        self.create_oval (depart_x, depart_y,
                                        depart_x + self.taille - 2*self.bordure_ronds,
                                        depart_y + self.taille - 2*self.bordure_ronds,
                                        fill= piece.color, outline=piece.color)
                else :
                    nb_cases_vides += 1
                    if self.type_affichage == "rond" :
                        self.create_oval (depart_x, depart_y,
                                    depart_x + self.taille - 2*self.bordure_ronds,
                                    depart_y + self.taille - 2*self.bordure_ronds,
                                    fill= self.color)
                        
        if self.type_affichage == "carre" :
            self.create_rectangle (self.origine_x, self.origine_y,
                                   self.origine_x+self.taille*(self.boss.grille_x),
                                   self.origine_y+self.taille*(self.boss.grille_y),
                                   outline= self.color_grille,
                                   width= self.taille_contours_grille)
        if nb_cases_vides == 0 :
            showinfo ('Félicitations !!','Vous avez brillement réussi à remplir complètement le puzzle !!!')




    def barre_verticale (self, ox, oy, t, color, taille) :
        "Trace dans le canvas une ligne verticale"
        self.create_line (ox,oy,ox,oy+t, fill= color, width=taille)


    def barre_horizontale (self, ox, oy, t, color, taille) :
        "Trace dans le canvas une ligne verticale"
        self.create_line (ox,oy,ox+t,oy, fill= color, width=taille)
    

    def refresh (self) :
        self.delete("all")
        self.trace_grille ()
        if self.boss.bases.nom :
            self.create_text(self.x/2, self.origine_y/2,
                             text=self.boss.bases.nom,
                             font= ("Calibri",int(5*log(self.boss.winfo_width()))),
                             fill="white")
    
    
    def couleurs (self) :
        if self.couleur_mode == "black" :
            #self["bg"] = "white"
            self.color = "white"
            self.color_grille = "black"
            self.couleur_mode = "white"
        elif self.couleur_mode == "white" :
            #self["bg"] = "black"
            self.color = "black"
            self.color_grille = "white"
            self.couleur_mode = "black"
        self.coutours_pour_bases()
        self.refresh()
        self.boss.scrollable_canvas.refresh()
    
    def coutours_pour_bases (self) :
        if self.boss.bases.nom :
            if self.boss.bases.nom[:7] == "Starter" :
                self["bg"] = "#59E81C"
            elif self.boss.bases.nom[:6] == "Junior" :
                self["bg"] = "#E8D717"
            elif self.boss.bases.nom[:6] == "Expert" :
                self["bg"] = "#FF0000"
            elif self.boss.bases.nom[:6] == "Master" :
                self["bg"] = "#AF32D9"
            elif self.boss.bases.nom[:6] == "Wizard" :
                self["bg"] = "#1A09D9"
        else :
            self["bg"] = self.color

    def change_type_affichage (self) :
        if self.type_affichage == "carre" :
            self.type_affichage = "rond"
        elif self.type_affichage == "rond" :
            self.type_affichage = "carre"
        self.refresh()
        self.boss.scrollable_canvas.refresh()
        
        
    def redimentionner (self) :
        self.x = self.winfo_width()
        self.y = self.winfo_height()
        self.taille_auto ()
        self.origines ()
        self.refresh ()


    def effacer_grille (self) :
        self.boss.bases.desactiver()
        self.boss.init_grille (self.boss.grille_x,self.boss.grille_y)
        self.refresh()
        self.boss.scrollable_canvas.init_pieces_affichees()
        self.boss.scrollable_canvas.refresh()


    def affiche_body_piece (self, piece) :
        self.refresh()
        piece.affichage (self, self.taille, 10, 10, self.bordure_ronds)
        self.piece_position = (10,10)
        self.deplace_body_piece = True
        self.piece_en_dep = 0
        self.piece = piece


    def case_cliquée (self,x_clic,y_clic) :
        "Restitue en fonction des coordonnés du clic la case cliquée"
        x = (x_clic-self.origine_x) // self.taille
        y = (y_clic-self.origine_y) // self.taille
        return int(x),int(y)


    def clic (self, event=None) :
        x,y = event.x,event.y
        if self.deplace_body_piece and \
           0 < x-self.piece_position[0] < self.piece.x*self.taille and \
           0 < y-self.piece_position[1] < self.piece.y*self.taille :
            self.piece_en_dep = 1
            self.x1, self.y1 = x, y
        elif self.boss.creation_pieces and \
           self.origine_x < x < self.origine_x + self.boss.grille_x * self.taille and \
           self.origine_y < y < self.origine_y + self.boss.grille_y * self.taille :
            x,y = self.case_cliquée (event.x,event.y)
            self.boss.grille[y][x] = ("Nouvelle piece",self.boss.colors[0])
            self.refresh()


    def mouseMove(self, event):
        "Op. à effectuer quand la souris se déplace, bouton gauche enfoncé"
        if self.piece_en_dep :
            self.piece_en_dep += 1
            x2, y2 = event.x, event.y
            dx, dy = x2 -self.x1, y2 -self.y1
            for el in self.piece.body[self] :
                self.move(el, dx, dy)
            self.piece_position = (self.piece_position[0]+dx, self.piece_position[1]+dy)
            self.x1, self.y1 = x2, y2
    
    
    def mouseUp(self, event):
        "Op. à effectuer quand le bouton gauche de la souris est relâché"
        if self.piece_en_dep :
            if self.piece_en_dep == 1 :
                self.piece.suppr(self)
                self.piece.position_suivante()
                self.piece.affichage (self, self.taille,
                             self.piece_position[0], self.piece_position[1],
                             self.bordure_ronds)
            else :
                x = self.piece_position[0] + self.taille/2
                y = self.piece_position[1] + self.taille/2
                if 0 < x - self.origine_x <  (self.piece.pos_max_x+1) * self.taille and \
                   0 < y - self.origine_y <  (self.piece.pos_max_y+1) * self.taille :
                    x,y = self.case_cliquée (x,y)
                    if self.boss.solver.position_possible (self.piece, (x,y)) :
                        self.deplace_body_piece = False
                        self.boss.inser_piece((x,y),piece=self.piece)
                        self.refresh()
            self.piece_en_dep = 0


    def double_clic (self, event=None) :
        x,y = event.x,event.y
        if self.origine_x < x < self.origine_x + self.boss.grille_x * self.taille and \
           self.origine_y < y < self.origine_y + self.boss.grille_y * self.taille :
            x,y = self.case_cliquée (event.x,event.y)
            if self.boss.grille[y][x] != "0" :
                piece = self.boss.grille[y][x]
                MsgBox = askquestion ('Supprimer une piece',
                                                'Voulez-vous vraiment supprimer la piece "'+piece.nom+'" ?',icon = 'warning')
                if MsgBox == 'yes':
                    self.boss.retirer_piece(piece)
                    self.refresh()


    def fleche_haut (self, event=None) :
        if self.deplace_body_piece and not(self.piece_en_dep) :
            self.piece.suppr(self)
            self.piece.retourner_haut_bas()
            self.piece.affichage (self, self.taille,
                             self.piece_position[0], self.piece_position[1],
                             self.bordure_ronds)
    
    def fleche_bas (self, event=None) :
        if self.deplace_body_piece and not(self.piece_en_dep) :
            self.piece.suppr(self)
            self.piece.retourner_droite_gauche()
            self.piece.affichage (self, self.taille,
                             self.piece_position[0], self.piece_position[1],
                             self.bordure_ronds)
    
    def fleche_droite (self, event=None) :
        if self.deplace_body_piece and not(self.piece_en_dep) :
            self.piece.suppr(self)
            self.piece.turn_right()
            self.piece.affichage (self, self.taille,
                             self.piece_position[0], self.piece_position[1],
                             self.bordure_ronds)
    
    def fleche_gauche (self, event=None) :
        if self.deplace_body_piece and not(self.piece_en_dep) :
            self.piece.suppr(self)
            self.piece.turn_left()
            self.piece.affichage (self, self.taille,
                             self.piece_position[0], self.piece_position[1],
                             self.bordure_ronds)











def ouvrir_docu_pieces () :
    nom = "Pieces/#docu pieces"
    fichier = open (nom, "r")
    table = []
    for ligne in fichier :
        ligne = ligne.rstrip()
        table.append(ligne)
    fichier.close()
    return table

class Piece () :
    docu_pieces = ouvrir_docu_pieces ()
    
    def __init__(self, boss=None, num=0, color="black", source=None) :
        self.boss = boss
        self.color = color
        if source == None :
            p = Piece.docu_pieces
        else :
            p = source
        self.ouvrir (p[num])
        self.init_positions_possibles()
        self.nb_boules = self.nb_boules_par_piece(self.grille)
        
        self.taille_inter_boules = 4/10 # peut changer (unité en pourcentage de la boule)
        self.taille_exter_boules = (1-self.taille_inter_boules)/2
        self.truc_utile = sqrt(1-self.taille_inter_boules**2)
        
        self.init_toutes_positions_possibles()
              
    def fin_init (self) :
        self.num = self.boss.pieces_nom[self.nom][1]
        
    def ouvrir (self,nom_piece) :
        fichier = open ("Pieces/"+nom_piece, "r")
        table = []
        for ligne in fichier :
            ligne = ligne.rstrip()
            tab = ligne.split(",")
            table.append(tab)
        fichier.close()
        self.grille = table
        self.init_tailles()
        self.nom = nom_piece
    
    def nb_boules_par_piece (self, grille) :
        nb = 0
        for j in range (len(grille)) :
            for i in range (len(grille[0])) :
                if grille[j][i] == "1" :
                    nb += 1
        return nb
      
    def init_tailles (self) :
        self.x = len(self.grille[0])
        self.y = len(self.grille)
        self.init_positions_possibles()
     
    def init_positions_possibles (self) :
        self.pos_max_x = self.boss.grille_x - self.x
        self.pos_max_y = self.boss.grille_y - self.y
    
    def suppr (self, canvas) :
        for el in self.body[canvas] :
            canvas.delete(el)
        self.body[canvas] = []
    
    def init_toutes_positions_possibles (self) :
        self.pos_possibles = []
        self.ajout_pos()
        self.retourner_haut_bas()
        self.ajout_pos()
        self.retourner_droite_gauche()
        self.ajout_pos()
        """
        print(self.nom)
        for el in self.pos_possibles :
            print(el)
        print()
        """
        self.grille = self.pos_possibles[0].copy()
        self.pos_num = 0
        self.init_tailles()
        
    def ajout_pos (self) :
        for i in range (4) :
            self.turn_right ()
            if not(self.grille in self.pos_possibles) :
                self.pos_possibles.append(self.grille.copy())
    
    def position_suivante (self) :
        self.pos_num = self.pos_possibles.index(self.grille)
        self.pos_num = (self.pos_num + 1) % len(self.pos_possibles)
        self.grille = self.pos_possibles[self.pos_num].copy()
        self.init_tailles()
       
    def turn_left (self) :
        g = []
        for i in range (self.x-1,-1,-1) :
            a = []
            for j in range (self.y) :
                a.append(self.grille[j][i])
            g.append(a)
        assert self.nb_boules == self.nb_boules_par_piece(g)
        self.grille = g
        self.init_tailles()
        
    def turn_right (self) :
        g = []
        for i in range (self.x) :
            a = []
            for j in range (self.y-1,-1,-1) :
                a.append(self.grille[j][i])
            g.append(a)
        assert self.nb_boules == self.nb_boules_par_piece(g)
        self.grille = g
        self.init_tailles()
    
    def retourner_haut_bas (self) :
        g = []
        for j in range (self.y-1,-1,-1) :
            g.append(self.grille[j])
        assert self.nb_boules == self.nb_boules_par_piece(g)
        self.grille = g
        self.init_tailles()
    
    def retourner_droite_gauche (self) :
        g = []
        for j in range (self.y) :
            a = []
            for i in range (self.x-1,-1,-1) :
                a.append(self.grille[j][i])
            g.append(a)
        assert self.nb_boules == self.nb_boules_par_piece(g)
        self.grille = g
        self.init_tailles()
    
    
    def affichage (self, canvas, t, ox, oy, bordure_ronds) :
        "Créer et affiche le body de la piece"
        self.body = {}
        self.body[canvas] = []
        truc_utile = self.truc_utile * (t-2*bordure_ronds)/2
        for j in range (self.y) :
            for i in range (self.x) :
                if self.boss.canvas.type_affichage == "rond" :
                    add = bordure_ronds
                else :
                    add = 0
                depart_x = ox + t * i + add
                depart_y = oy + t * j + add
                if self.grille[j][i] == "1" :
                    if self.boss.canvas.type_affichage == "carre" :
                        self.body[canvas].append(canvas.create_rectangle (depart_x, depart_y,
                                               depart_x + t, depart_y + t,
                                               fill= self.color,
                                               outline=self.boss.canvas.color_grille))
                    elif self.boss.canvas.type_affichage == "rond" :
                        self.body[canvas].append(canvas.create_oval (depart_x, depart_y,
                                        depart_x + t - 2*bordure_ronds,
                                        depart_y + t - 2*bordure_ronds,
                                        fill= self.color, outline=self.boss.canvas.color_grille))
        if self.boss.canvas.type_affichage == "rond" :
            for j in range (self.y) :
                for i in range (self.x) :
                    if self.boss.canvas.type_affichage == "rond" :
                        add = bordure_ronds
                    else :
                        add = 0
                    depart_x = ox + t * i + add
                    depart_y = oy + t * j + add
                    if self.grille[j][i] == "1" :    
                        if i < self.x-1 and \
                           self.grille[j][i+1] != "0" and \
                           self.grille[j][i+1] == self.grille[j][i] :
                            depart_x2 = depart_x+(t-2*bordure_ronds)/2
                            depart_y2 = depart_y+(t-2*bordure_ronds)*self.taille_exter_boules
                            self.body[canvas].append(canvas.create_rectangle (depart_x2, depart_y2,
                                                   depart_x2 + (t-2*bordure_ronds),
                                                   depart_y2 + (t-2*bordure_ronds)*self.taille_inter_boules ,
                                                   fill= self.color, outline=self.color))
                            self.body[canvas].append(canvas.create_line(depart_x2 + truc_utile,
                                                                        depart_y2,
                                                                        depart_x2 + t-truc_utile,
                                                                        depart_y2,
                                                                        fill=self.boss.canvas.color_grille))
                            self.body[canvas].append(canvas.create_line(depart_x2 + truc_utile,
                                                                        depart_y2 + (t-2*bordure_ronds)*self.taille_inter_boules,
                                                                        depart_x2 + t-truc_utile,
                                                                        depart_y2 + (t-2*bordure_ronds)*self.taille_inter_boules,
                                                                        fill=self.boss.canvas.color_grille))
                        if j < self.y-1 and \
                           self.grille[j+1][i] != "0" and \
                           self.grille[j+1][i] == self.grille[j][i] :
                            depart_x2 = depart_x+(t-2*bordure_ronds)*self.taille_exter_boules
                            depart_y2 = depart_y+(t-2*bordure_ronds)/2
                            self.body[canvas].append(canvas.create_rectangle (depart_x2, depart_y2,
                                                   depart_x2 + (t-2*bordure_ronds)*self.taille_inter_boules,
                                                   depart_y2 + (t-2*bordure_ronds) ,
                                                   fill= self.color, outline=self.color))
                            self.body[canvas].append(canvas.create_line(depart_x2,
                                                                        depart_y2 + truc_utile,
                                                                        depart_x2,
                                                                        depart_y2 + t-truc_utile,
                                                                        fill=self.boss.canvas.color_grille))
                            self.body[canvas].append(canvas.create_line(depart_x2 + (t-2*bordure_ronds)*self.taille_inter_boules,
                                                                        depart_y2 + truc_utile,
                                                                        depart_x2 + (t-2*bordure_ronds)*self.taille_inter_boules,
                                                                        depart_y2 + t-truc_utile,
                                                                        fill=self.boss.canvas.color_grille))
                        

class Boutons(Frame) :
    def __init__(self,boss=None) :
        Frame.__init__(self,boss)
        self.boss = boss
        self.nb_lignes = 12
        self.grid_columnconfigure(0, weight= 1, minsize= (1-self.boss.proportion_canvas_x)*self.boss.min_x)
        for i in range (self.nb_lignes) :
            self.grid_rowconfigure(i, weight= 1, minsize= 1/self.nb_lignes*self.boss.min_y)
        
        
        self.items = ["0"]*11
        
        self.items[0] = Button (self, text='Couleurs', command=self.boss.canvas.couleurs)
        self.items[0].grid(row= 0)
        
        self.items[5] = Button (self, text='Type\naffichage', command=self.boss.canvas.change_type_affichage)
        self.items[5].grid(row= 1)
        
        self.text_creer_piece = StringVar()
        self.text_creer_piece.set("Créer Piece")
        self.items[1] = Button (self, textvariable=self.text_creer_piece, command=self.boss.creer_piece)
        self.items[1].grid(row= 3)
        self.items[2] = Button (self, text='Enregistrer', command=self.boss.enregistrer_piece)
        
        self.bases = Frame(self)
        self.bases.grid(row=6)
        self.items[8] = Button (self.bases, text='<-', command=self.boss.bases.bases_moins)
        self.items[8].pack(side="left")
        self.items[9] = Button (self.bases, text='Bases', command=self.boss.bases.bases_on_off)
        self.items[9].pack(side="left")
        self.items[10] = Button (self.bases, text='->', command=self.boss.bases.bases_plus)
        self.items[10].pack(side="left")
        
        self.items[7] = Button (self, text='Enregistrer\ncomme base', command=self.boss.bases.enregistrer_comme_base)
        self.items[7].grid(row= 7)
        
        self.items[3] = Button (self, text='Effacer', command=self.boss.canvas.effacer_grille)
        self.items[3].grid(row= 9)
        
        self.items[4] = Button (self, text='Changer\ntaille grille', command=self.boss.change_taille_grille)
        self.items[4].grid(row= 10)
        
        self.items[6] = Button (self, bg="blue", text='Résoudre', command=self.boss.solver.resoudre,fg="white")
        self.items[6].grid(row= 11, padx= 1/90*self.boss.x,
                           pady= 1/90*self.boss.x, sticky=NSEW)
        self.cacher_enregistrer()

    def redimentionner (self) :
        text_size = int(5*log(self.boss.winfo_width()/100))
        for bout in self.items :
            bout.config(font=("Verdana", text_size))
                     
    def afficher_enregistrer (self) :
        self.items[2].grid(row= 4)
    def cacher_enregistrer (self) :
        self.items[2].grid_forget()


class ScrollableCanvas(Frame):
    def __init__(self, boss=None, x=500,y=100):
        Frame.__init__(self, boss)
        self.boss = boss
        self.x = x
        self.y = y
        self.longeur_canvas = x
        self.canvas=Canvas(self, width=x, height=y, scrollregion=(0,0,self.longeur_canvas,y))

        self.init_pieces_affichees()
        
        vbar=Scrollbar(self,orient=HORIZONTAL)
        vbar.pack(side=BOTTOM, fill=X)
        vbar.config(command=self.canvas.xview)
         
        self.canvas.config(xscrollcommand=vbar.set)
        self.canvas.pack(side=TOP,expand=True)
        self.canvas.bind("<Button-1>",self.clic)
        #self.canvas.bind("<Double-Button-1>",self.coucou)
        
    def coucou (self,event=None) :
        print("ok")
    
    def init_pieces_affichees (self) :
        self.pieces_affichees = self.boss.pieces.copy()
    
    def piece_cliquée (self,x_clic,y_clic) :
        "Restitue en fonction des coordonnés du clic la piece cliquée"
        for el in self.position_pieces :
            if el[0][0] < x_clic < el[1][0] and el[0][1] < y_clic < el[1][1] :
                return (True,el[2])
        return (False,)

    def clic (self, event=None) :
        x,y = self.canvas.canvasx(event.x),event.y
        a = self.piece_cliquée (x,y)
        if a[0] :
            if self.boss.creation_pieces :
                showinfo ('Erreur','La fonction "Placer la piece" n´est pas disponible car le mode "Création de pieces" est activé !',icon = 'error')
            else :
                self.boss.canvas.affiche_body_piece(a[1])
                      
    def redimentionner (self) :
        self.x = self.winfo_width()
        self.y = self.winfo_height()
        self.canvas.config(width=self.x, height=self.y)
        self.refresh()
             
    def refresh (self) :
        self.canvas.delete("all")
        self.trace_pieces()
        if self.boss.canvas.couleur_mode == "white" :
            self.canvas["bg"] = "#D4D4D4"
            self["bg"] = "#D4D4D4"
        elif self.boss.canvas.couleur_mode == "black" :
            self.canvas["bg"] = "#595959"
            self["bg"] = "#595959"
 
    def taille_auto (self, grille_y, distance_piece_canvas) :
        "Calcule la taille en pixel d´un coté des cases carré à partir de la hauteur h et le la longeur l de la grille de définition"
        taille = self.y / (grille_y+2*distance_piece_canvas)
        bordure_ronds = 1/10*taille
        return taille, bordure_ronds

    def trace_pieces (self) :
        "Trace avec Tkinter les pieces disponibles dans le canvas"
        self.position_pieces = []
        self.ox = self.oy = 0
        for piece in self.pieces_affichees :
            if piece != None :
                self.ajout_piece(piece)

    def ajout_piece (self, piece) :
        if self.boss.canvas.type_affichage == "carre" :
            distance_piece_canvas = 1 # unité en nombre de t
        elif self.boss.canvas.type_affichage == "rond" :
            distance_piece_canvas = 0.75
        t, br = self.taille_auto(piece.y,distance_piece_canvas)
        pos_initiale = (self.ox+t,self.oy+t)
        piece.affichage (self.canvas, t,self.ox+t*distance_piece_canvas,
                         self.oy+t*distance_piece_canvas, br)
        self.ox += t* (piece.x+1)
        self.oy = 0
        pos_finale = (self.ox, t*(piece.y+1))
        self.position_pieces.append((pos_initiale,pos_finale,piece))
        self.longeur_canvas = self.ox +t
        self.canvas.config(scrollregion=(0,0,self.longeur_canvas,self.y))


class Solver () :
    def __init__(self, boss=None) :
        self.boss = boss
    
    
    def init_pieces (self) :
        self.pieces = []
        for el in self.boss.scrollable_canvas.pieces_affichees :
            if el != None :
                self.pieces.append(el)
    
    
    def init_cases_libres (self) :
        self.cases_libres = []
        for j in range (len(self.grille)) :
            for i in range (len(self.grille[0])) :
                if self.grille[j][i] == "0" :
                    self.cases_libres.append((i,j))
    
    
    def position_possible (self, piece, position) :
        x = position[0]
        y = position[1]
        for j in range (piece.y) :
            for i in range (piece.x) :
                if piece.grille[j][i] == "1" and self.boss.grille[y+j][x+i] != "0" :
                    return False
        return True
    
    def init_positions_possibles_par_pieces (self) :
        self.positions_possibles_par_pieces = {}
        for piece in self.pieces :
            self.positions_possibles_par_pieces[piece] = {}
            for orientation in piece.pos_possibles :
                for pos in self.cases_libres :
                    if pos[0]< piece.pos_max_x and pos[0]< piece.pos_max_x :
                        for y in range (piece.y) :
                            for x in range (piece.x) :
                                pass
                                
                    
    
    
    def inser_piece (self, pos, piece=0, num_piece=0) :
        pass
        """if not(piece) :
            piece = self.pieces[num_piece]
        for j in range (piece.y) :
            for i in range (piece.x) :
                if piece.grille[j][i] == "1" :
                    self.grille[pos[1]+j][pos[0]+i] = piece
        self.scrollable_canvas.pieces_affichees[piece.num] = None
        self.scrollable_canvas.refresh()"""
        
    
    def resoudre (self) :
        if self.boss.creation_pieces :
            showinfo ('Erreur','La fonction "Resoudre" n´est pas disponible car le mode "Création de pieces" est activé !',icon = 'error')
        else :
            self.archive_grilles = []
            self.grille = self.boss.grille.copy()
            self.init_pieces()
            self.init_cases_libres()
            self.init_positions_possibles_par_pieces()
        return self.grille






if __name__ == "__main__" :
    fen = Fenetre()
    fen.mainloop()