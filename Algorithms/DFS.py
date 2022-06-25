from copy import deepcopy 

#Création des variables 
t=[[1,2,3],[8,6,0],[7,5,4]]
tf=[[1,2,3],[8,0,4],[7,6,5]]
liste=deepcopy(t)

#Fonction qui affiche la matrice
def affiche(liste):
  print("+---+---+---+") 
  for i in range(3) :
    print("|",liste[i][0],"|",liste[i][1],"|",liste[i][2],"|")
    print("+---+---+---+")
  

#Fonction qui retourne l'état initial
def etat_depart():
  return t 

#Fonction qui retourne l'état final
def etat_final(t,tf) : 
   if (t==tf) : 
        return True 
   else : 
        return False 

#Fonction qui retourne la position du case_vide
def position_case_vide(t) : 
  for i in range(3): 
    for j in range(3) : 
      if t[i][j]==0 : 
        return i,j

#Fonction qui retourne la valeur du case spécifique
def numero(t,x,y): 
  return t[x][y]

#Fonction qui permet d'échanger deux cases
def permuter( t , c1 , c2): 
  aux = t[c1[0]][c1[1]]
  t[c1[0]][c1[1]]=t[c2[0]][c2[1]]
  t[c2[0]][c2[1]]=aux
  return t 

#Fonction qui tourne tous les cases possibles de transition 
def transition(t) : 
  li=[]
  d1=[1,0,-1,0]
  d2=[0,1,0,-1]
  k1,k2= position_case_vide(t)
  for i in range(4): 
    m=[k1+d1[i],k2+d2[i]]
    if m[0]>=0 and m[0]<3 : 
       if m[1]>=0 and m[1]<3 : 
         li.append(m)
  return li 

#Fonction qui tourne les matriices des cas possibles de transition 
def successorsOf(t) : 
  resultat=[]
  succ= transition(t) 
  for i in range(len(succ)) : 
    cp= deepcopy(t)
    k1,k2= position_case_vide(t) 
    resultat.append(permuter(cp,[k1,k2],succ[i]))
  return resultat

#Fonction qui fait les pas possibles pour avoir l'etat final par la recherche en largeur et en profondeur
def recherche(t,goal,DFS_BFS) : # True : en largeur , False : en profendeur
  freeNodes=[]
  freeNodes.append(t)
  closedNodes=[]
  path=[]
  success=False
  pas=0
  while len(freeNodes)!=0 and success==False : 
    generate=[]
    firstNode=freeNodes[0]
    path.append(firstNode)
    pas+=1
    freeNodes.remove(firstNode)
    closedNodes.append(firstNode)
    generate=successorsOf(firstNode)
    for i in generate : 
      if i in freeNodes or i in closedNodes: 
        generate.remove(i)

    for i in generate : 
      test=etat_final(i,goal)
      if(test ==True) :
        path.append(i)
        success=True
        goalNode=i
    if DFS_BFS==True : 
      for i in freeNodes : 
        generate.append(i)
      freeNodes = generate
    else : 
        for i in generate : 
          freeNodes.append(i)
     
  return path

def recherchel(t,goal,limit) : # profondeur limité
  freeNodes=[]
  freeNodes.append(t)
  closedNodes=[]
  goalNode=[]
  path=[]
  success=False
  pas=0
  while (len(freeNodes)!=0) and (success==False) and (pas<=limit) : 
    generate=[]
    firstNode=freeNodes[0]
    path.append(firstNode)
    pas+=1
    freeNodes.remove(firstNode)
    closedNodes.append(firstNode)
    generate=successorsOf(firstNode)
    for i in generate : 
      if i in freeNodes or i in closedNodes: 
        generate.remove(i)
    print(pas,limit)
    affiche(firstNode)
    for i in generate : 
      test=etat_final(i,goal)
      if((test==True) and (pas+1<=limit)) :
        success=True
        goalNode=i
        path.append(i)

    for i in freeNodes : 
        generate.append(i)
    freeNodes = generate
    
  return   path

#Fonction donne le nb des cases mal placés 
def h(tc,tf):
  mp=0 
  for i in range(3):
    for j in range(3): 
      if (tc[i][j]!= tf[i][j]) and (tc[i][j]!=0):
        mp=mp+1
  return mp

#Fonction qui fait les pas possibles pour avoir l'etat final par la recherche A*
def recherche2(t,tf):
  open=[]
  close=[]
  niveau= 0
  success = False
  path=[]
  open.append(t)
  while open!=[] and success==False :
    noeud = open[0]
    niveau+=1
    close.append(noeud)
    open.remove(noeud)
    path.append(noeud)
    if etat_final(noeud,tf):
      success = True
    else :
      childs=successorsOf(noeud)
      for child in childs : 
        if (child in open) or(child in close):
            childs.remove(child)
    open=open+childs
    open.sort(key=lambda e:(niveau+h(e,tf)))
  return path

#interface graphique pour jouer taquin
from tkinter import *

def show(titre,liste,maxx,p):

      if (p<maxx):
          FONT=('Ubuntu', 27, 'bold')
          master=Tk()
          master.title(titre)
          cnv=Canvas(master, width=300, height=300, bg='gray70')
          cnv.pack(side=TOP, padx=5, pady=5)        
          def init(p,btn1,btn,l):
           p=0
           cnv.delete("all")
           tc=liste[0]
           for i in range(3):
            for j in range(3):
               if tc[i][j]!=0 :
                   x, y=100*j, 100*i
                   A, B, C=(x, y), (x+100, y+100), (x+50, y+50)
                   cnv.create_rectangle(A, B, fill="royal blue")
                   cnv.create_text(C, text=tc[i][j], fill="yellow", font=FONT)
           btn1.destroy()
           l.destroy()
           btn.destroy()           
           l = Label(text = "Pas =0")
           l.pack()
           btn=Button(text="Depart", command=lambda :init(p,btn,btn1,l))
           btn.pack(side=LEFT, padx=5, pady=5)
           btn1=Button(text="next", command=lambda :f(1,btn1,btn,l))
           btn1.pack(side=RIGHT, padx=5, pady=5)

          def f(p,btn1,btn,l):
           if p<len(liste):
             cnv.delete("all")
             tc=liste[p]
             for i in range(3):
               for j in range(3):
                 if tc[i][j]!=0 :
                   x, y=100*j, 100*i
                   A, B, C=(x, y), (x+100, y+100), (x+50, y+50)
                   cnv.create_rectangle(A, B, fill="royal blue")
                   cnv.create_text(C, text=tc[i][j], fill="yellow", font=FONT)
             btn1.destroy()
             l.destroy()
             btn.destroy()
             p=p+1
             if p==len(liste) :
                   t="Pas ="+str(p-1)
                   tf=" --- FIN - "+t+" ---"
                   l = Label(text = tf)
                   l.pack()
                   btn=Button(text="Depart", command=lambda :init(p,btn,btn1,l))
                   btn.pack(side=LEFT, padx=5, pady=5)                   
                   btn1=Button(text="next", command=lambda :f(p,btn1,btn,l))
                   btn1.pack(side=RIGHT, padx=5, pady=5)
             else :
                   t="Pas ="+str(p-1)
                   #fg ='red', bg ='white'
                   l = Label(text = t )
                   l.pack()
                   btn=Button(text="Depart", command=lambda :init(p,btn,btn1,l))
                   btn.pack(side=LEFT, padx=5, pady=5)
                   btn1=Button(text="next", command=lambda :f(p,btn1,btn,l))
                   btn1.pack(side=RIGHT, padx=5, pady=5)
           else :
               f(maxx-1,btn1,btn,l)

          tc=liste[p]
          p+=1
          for i in range(3):
            for j in range(3):
               if tc[i][j]!=0 :
                   x, y=100*j, 100*i
                   A, B, C=(x, y), (x+100, y+100), (x+50, y+50)
                   cnv.create_rectangle(A, B, fill="royal blue")
                   cnv.create_text(C, text=tc[i][j], fill="yellow", font=FONT)
          l = Label(text = "Pas=0")
          l.pack()
          btn1=Button(text="next", command=lambda :f(p,btn,btn1,l))
          btn1.pack(side=RIGHT, padx=5, pady=5)
          btn=Button(text="Depart", command=lambda :init(p,btn,btn1,l))
          btn.pack(side=LEFT, padx=5, pady=5)

          master.mainloop()


def graphe(titre,liste):
    show(titre,liste,len(liste),0)

#main
# Pas:5
#graphe("Recherche en largeur ",recherche(t,tf,False))

# Pas:3
#graphe("Recherche en profondeur ",recherche(t,tf,True))

# Pas:2(limit)
graphe("Recherche en profondeur limité",recherchel(t,tf,1)) 

# Pas:3
#graphe("Recherche en A*",recherche2(t,tf))




