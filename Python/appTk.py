import tkinter as tk
from tkinter import filedialog

import numpy as np
import matplotlib.pyplot as plt

from docplex.mp.model import Model

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    entry_var.set(file_path)
    read_file(file_path)

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            text_var.set(content)  # Store content in a variable
            text = text_var.get()
            text_widget.delete('1.0', tk.END)  # Clear previous content
            text_widget.insert(tk.END, content)
    except Exception as e:
        text_var.set(f"Error: {str(e)}")

def solve():
        print('Résolution...')
        Xclient = []
        Yclient = []
        demandeClient = [0]
        
        lignes = text_var.get().split('\n')
        cpt = 0
        for ligne in lignes:
            if cpt == 0:
                temp = ligne.split(' ')
                C = int(temp[0])
                V = int(temp[1])

                cpt+=1
                continue

            if cpt == 1:
                Q = int(ligne)
                cpt+=1
                continue

            if cpt == 2:
                Xdepot = int(ligne.split(' ')[0])
                Ydepot = int(ligne.split(' ')[1])
                cpt+=1
                continue

            tab = ligne.split(' ')
            Xclient.append(int(tab[1]))
            Yclient.append(int(tab[2]))
            demandeClient.append(int(tab[3]))

            cpt+=1
        
        Vehicles = [i for i in range(1, V+1)]
        N = [i for i in range(1, C+1)]
        print(N)
        Vertices = [0] + N
        demande = demandeClient
        print(demande)
        loc_x = [Xdepot]+Xclient
        loc_y = [Ydepot]+Yclient
        print(loc_x)
        print(loc_y)

        A = [(i, j) for i in Vertices for j in Vertices if i!=j]
        B = [(i, j, v) for i in Vertices for j in Vertices for v in Vehicles if i!=j]
        print(B)
        dist = {(i, j): np.hypot(loc_x[i]-loc_x[j], loc_y[i]-loc_y[j]) for i in Vertices for j in Vertices}
        print(dist)
        
        # Modélisation mathématique
        mdl = Model('CVRP')
        x = mdl.binary_var_dict(B, name='x')
        u = mdl.continuous_var_dict(N, ub=Q, name='u')
        
        mdl.minimize(mdl.sum(dist[i, j]*x[i, j,v]  for i, j,v in B))
        mdl.add_constraint(mdl.sum(x[0,j,v] for j in N for v in Vehicles)>=1)#Au moins 1 véhicules utilisés
        mdl.add_constraints(mdl.sum(x[j,0,v] for j in N)<=1 for v in Vehicles)#Les véhicules si il quitte le dépôt, il rentrera au dépôt à la fin
        mdl.add_constraints(mdl.sum(x[j,0,v] for j in N)==mdl.sum(x[0,j,v] for j in N) for v in Vehicles) #Les véhicules si il quitte le dépôt, il rentrera au dépôt à la fin
        #Tous les véhicules quittent la node qu'il a visité
        mdl.add_constraints(mdl.sum(x[j,i,v] for i in Vertices if i!=j)== mdl.sum(x[i,j,v] for i in Vertices if i!=j) for j in Vertices for v in Vehicles)
        #Chaque client est passé par exactement 1 fois
        mdl.add_constraints(mdl.sum(x[i,j,v] for v in Vehicles for i in Vertices if i!=j) == 1 for j in N)
        #La capacité ne doit pas être dépassé
        mdl.add_constraints(mdl.sum(demande[j]*x[i,j,v] for i in Vertices for j in N if i!=j)<=Q for v in Vehicles)
        mdl.add_constraints(u[j]-u[i] >= demande[j]-Q*(1-x[i,j,v]) for i in N for j in N for v in Vehicles if i!=j)
        mdl.add_constraints(u[i]<= Q for i in N)
        mdl.add_constraints(u[i] >= demande[i] for i in N)
        solution = mdl.solve(log_output=True)
        #add_contraint et add_contraints => for chaque
        
        print(solution)
        
        solution.solve_status
        
        active_arcs = [a for a in B if x[a].solution_value > 0.9]
        print (active_arcs)
        
        # Définition de couleurs aléatoires
        color = np.random.rand(len(Vehicles), 3)
        
        
        plt.scatter(loc_x[1:], loc_y[1:], c='b')
        for i in N:
            plt.annotate('$n_%d=%d$' % (i, demande[i]), (loc_x[i]+2, loc_y[i]))
        for i, j,v in active_arcs:
            plt.plot([loc_x[i], loc_x[j]], [loc_y[i], loc_y[j]], c=color[v-1], alpha=0.3)
        plt.plot(loc_x[0], loc_y[0], c='r', marker='s')
        plt.axis('equal')
        plt.show()

# Function to print the content variable
def print_content():
    print(text_var.get())

# Create the main window
root = tk.Tk()
root.title("Text File Reader")

# Create a label
label = tk.Label(root, text="Select a text file:")
label.pack(pady=10)

# Create an entry to display the selected file path
entry_var = tk.StringVar()
entry = tk.Entry(root, textvariable=entry_var, state='readonly', width=40)
entry.pack(pady=10)

# Create a button to open file dialog
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack(pady=10)

# Create a text widget to display file content
text_var = tk.StringVar()
text_widget = tk.Text(root, height=10, width=50)
text_widget.pack(pady=10)

# Create a button to print the content variable
print_button = tk.Button(root, text="Résoudre avec CPlex", command=solve)
print_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()