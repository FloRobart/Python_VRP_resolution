import numpy as np
from docplex.mp.model import Model
import matplotlib.pyplot as plt

#Problèmes
# D : dépôt
# C : clients
# V : véhicules
# 𝐷𝑖𝑠𝑡(ij) : distance entre les nœuds (clients ou dépôt) i et j
# 𝑑𝑒𝑚𝑎𝑛𝑑𝑒(i) : demande du client i
# 𝑄𝑚𝑎𝑥(v): Capacité du véhicule v

# Variables fournies
# 4 véhicules, 10 clients et 1 dépôt
# Demandes des clients [60,18,26,15,44,32,20,10,27,11]
# Capacité max d’un véhicule : 100
# Matrice des distances :
# [[0 2.7 4.6 2.8 3 3.3 3.1 2.7 5.1 3.9 4.7],
# [2.7 0 3.1 0.8 1.8 2.5 4.2 1.4 3.6 2.5 3],
# [4.6 3.1 0 3.3 4.4 1.7 6.8 4.1 1.3 1.7 1.4],
# [2.8 0.8 3.3 0 1.9 2 4 1.5 3.8 2.8 3.2],
# [3 1.8 4.4 1.9 0 3.4 2.6 0.5 4.7 4.7 4.1],
# [3.3 2.5 1.7 2 3.4 0 5.8 3 1.8 0.5 2.6],
# [3.1 4.2 6.8 4 2.6 5.8 0 3 7.4 6.1 7.6],
# [2.7 1.4 4.1 1.5 0.5 3 3 0 4.6 3.7 4.3],
# [5.1 3.6 1.3 3.8 4.7 1.8 7.4 4.6 0 1.4 2.8],
# [3.9 2.5 1.7 2.8 4.7 0.5 6.1 3.7 1.4 0 2.8],
# [4.7 3 1.4 3.2 4.1 2.6 7.6 4.3 2.8 2.8 0]]



# Variables du programme
# n is the number of clientes
# N is set of clients, with N={1,2,...,n}
# V is set of vetices (or nodes), with V={0} cup N
# A is set of arcs, with A={(i,j)in V^2 : i neq j}
# c_ij is cost of travel over arc (i,j) in A
# Q is the vehicle capacity
# q_i is the amount that has to be delivered to customer, i in N

# Then, the formulation is the following
# sum_{i,j in A} c_{ij} x_{ij}  -> min
# sum_{j in V , j neq i} x_{ij} = 1     i in N 
# sum_{i in V , i neq j} x_{ij} = 1     j in N
# if x_{ij}=1 => u_i + q_j = u_j     i,j in A : j neq 0, i neq 0
# q_i <= u_i <= Q     i in N
# x_{ij} in {0,1}     i,j in A




# Données du problème
n = 10 # Nombre de clients
Q = 100 # Capacité du véhicule
N = [i for i in range(1,n+1)] # Clients
V = [0] + N # Clients + dépôt (Nodes)
q = [0,60,18,26,15,44,32,20,10,27,11] # Demandes des clients


# Placement des clients aléatoirement
rnd = np.random
rnd.seed(0)
loc_x = rnd.rand(len(V)+1)*400
loc_y = rnd.rand(len(V)+1)*200

# Affichage des clients et du dépôt sur un plan
plt.figure(figsize=(12,6)) # Set la taille de la fenêtre
plt.scatter(loc_x[1:], loc_y[1:], c='b') # Affiche les clients (cercles bleus)
for i in N: 
    plt.annotate('$q_%d=%d$' % (i, q[i]), (loc_x[i]+2, loc_y[i])) # Affiche les demandes des clients (à côté des clients)
plt.plot(loc_x[0], loc_y[0], c='r', marker='s') # Affiche le dépôt (carré rouge)
plt.axis('equal') # Met les axes à l'échelle
# plt.show() # Affiche le plan

# Calcul des distances entre les clients et le dépôt
A = [(i,j) for i in V for j in V if i != j] # Arcs (i,j) possibles
c = {(i,j): np.hypot(loc_x[i]-loc_x[j], loc_y[i]-loc_y[j]) for i,j in A} # Coûts de déplacement

# Création du modèle
mdl = Model('CVRP')

# Variables
x = mdl.binary_var_dict(A, name="x") # x_{ij} vaut 1 si le véhicule emprunte l'arc (i,j), 0 sinon
u = mdl.continuous_var_dict(N, ub=Q, name="u") # u_i est la quantité de marchandises restantes après avoir visité le client i

# Fonction objectif
mdl.minimize(mdl.sum(c[i,j]*x[i,j] for i,j in A)) # Minimise la somme des coûts de déplacement

# Contraintes
mdl.add_constraints(mdl.sum(x[i,j] for j in V if j != i) == 1 for i in N) # Chaque client est visité une fois
mdl.add_constraints(mdl.sum(x[i,j] for i in V if i != j) == 1 for j in N) # Chaque client est quitté une fois
mdl.add_indicator_constraints(mdl.indicator_constraint(x[i,j], u[i] + q[j] == u[j]) for i,j in A if i != 0 and j != 0) # Contrainte de capacité (sous forme d'indicatrice)
mdl.add_constraints(u[i] >= q[i] for i in N) # Contrainte de capacité (u_i >= q_i)
# mdl.parameters.timelimit = 15 # Limite de temps 

# Résolution
solution = mdl.solve(log_output=True) # Résout le problème

# Nombre de voitures utilisées
nb_vehicules_utilises = sum(solution.get_value(f'x_0_{j}') for j in N if j != 0)

# Capacité restante des véhicules v au retour au dépôt
capacite_restante = {i: Q - solution.get_value(f'u_{i}') for i in N}

# Affichage du nombre de voitures utilisées
print("Nombre de véhicules utilisés :", nb_vehicules_utilises)

# Affichage de la capacité restante des véhicules au retour au dépôt
print("Capacité restante des véhicules au retour au dépôt :")
for i in N:
    print(f"Véhicule {i} : {capacite_restante[i]}")


# Affichage de la solution
print(solution) # Affiche la solution

solution.solve_status
active_arcs = [a for a in A if x[a].solution_value > 0.9]

plt.scatter(loc_x[1:], loc_y[1:], c='b')
for i in N:
    plt.annotate('$q_%d=%d$' % (i, q[i]), (loc_x[i]+2, loc_y[i]))
for i, j in active_arcs:
    plt.plot([loc_x[i], loc_x[j]], [loc_y[i], loc_y[j]], c='g', alpha=0.3)
plt.plot(loc_x[0], loc_y[0], c='r', marker='s')
plt.axis('equal')



plt.show() # Affiche le plan



