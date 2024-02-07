/*********************************************
 * OPL 22.1.1.0 Model
 * Author: ll211074
 * Creation Date: 7 nov. 2023 at 14:56:51
 *********************************************/

// Définition des villes
int nbVilles = 20; 

// Matrice des coûts entre les villes
range villes=1..nbVilles; // L'ensemble I

// c est le cout ou la distance entre les villes
float c[i in villes][j in villes] = rand(100);

// Variable de décision : 1 si l'arc est inclus, 0 sinon
dvar boolean x[villes][villes]; 

// Fonction objectif : minimiser la somme des coûts des arcs inclus
minimize sum(i in villes, j in villes) c[i][j] * x[i][j];

subject to{
  //Contraintes
  forall (j in villes) sum(i in villes) x[i][j] == 1;
  forall (i in villes) sum(j in villes) x[i][j] == 1;  
}  


// Affichage de la solution
execute {
  var a=1;
  for (var b=1;b<nbVilles +1 ; b++)
  {
    for (var c=1;c<nbVilles+1;c++)
    {
      if (x[a][c]>0)
      {
        write(a + "-->");
        a=c;
        if(a ==1)
        {
          write(a);
            b = nbVilles +1;
            break;
          }        
      }
    }
  }
}