/*********************************************
 * OPL 22.1.1.0 Model
 * Author: dt213544
 * Creation Date: 7 févr. 2024 at 12:58:14
 *********************************************/
//Données
int nombreNode=...;
int Q=...; //capacité max des véhicules
int V=...; //Nombre de véhicules
float demande[2..nombreNode]=...; //Demandes des clients
float dist[1..nombreNode][1..nombreNode]=...;  
dvar boolean x[1..nombreNode][1..nombreNode][1..V];

minimize sum(i in 1..nombreNode,j in 1..nombreNode,v in 1..V ) dist[i][j]*x[i][j][v];
dvar int+ u[2..nombreNode]; // u est un variable pour éliminer les sous tours
//Contrainte
subject to {
    // Il y a pas de chemin de node i vers lui même
  	forall (i in 1..nombreNode, v in 1..V){
  	  x[i][i][v] == 0;
  	}
  	// Au moins 1 véhicule utlisé
 	 sum(j in 1..nombreNode,v in 1..V) x[1][j][v] >= 1;
  	// Quitter dépôt, rentrer le dépôt à la fin
  	forall (v in 1..V){ 
  		sum(j in 2..nombreNode) x[j][1][v] == sum (j in 2..nombreNode) x[1][j][v];
  		sum(j in 2..nombreNode) x[j][1][v] <= 1;
	}  
  	// Tous les véhicules Quitte la node qu'il a visiter - nombre de fois un node est quiité = nombre de fois un node est visité
  	forall (j in 1..nombreNode,v in 1..V) {
  	  sum(i in 1..nombreNode)x[j][i][v] == sum (i in 1..nombreNode) x[i][j][v];
  	}
  	//Chaque client est "entré" par 1 fois
  	forall (j in 2..nombreNode) {
  	  sum(v in 1..V, i in 1.. nombreNode) x[i][j][v] == 1;
  	 }
  	//Capacité ne doit pas être dépassé
  	forall (v in 1..V) 
  	{
  	  	sum(i in 1..nombreNode, j in 2..nombreNode) demande[j]*x[i][j][v] <= Q;  
  	}
  	//Eliminer le sous-tours
  	forall (i in 2..nombreNode, j in 2..nombreNode, v in 1..V : i!=j)
  	{
  	  u[j]-u[i] >= demande[j] - Q*(1-x[i][j][v]);
  	}
  	forall (i in 2..nombreNode){
  	  demande[i] <= u[i];
  	  u[i] <= Q;
  	}
}

execute {
  // Pour chaque véhicule
  for (var v = 1; v <= V; v++) {
    writeln("Chemin du véhicule ", v, ": ");
    
    // Trouver le chemin parcouru par le véhicule v
    var i = 1; // Départ du dépôt
    var j = 0;
    
    var sommeDemande = 0;
    write("Dépôt ", i);
    // Tant que le véhicule n'est pas retourné au dépôt
    while (j != 1) {
      // Trouver le prochain nœud j dans le chemin du véhicule v
      for (var k = 1; k <= nombreNode; k++) {
        
        if(i == 0){
          j = 1;
          break;
        }
        
        if (x[i][k][v] == 1) {
          j = k;
          //affichage des noeuds
          if(j == 1) {
            write("-> Dépôt ", j);
          }
          else {
            write(" -> Client ", j, " Distance ", i, " vers ", j, " : ", dist[i][j]);
            sommeDemande += demande[j];   
          }
           
              break;
        }
      }
      
      // Mettre à jour le nœud de départ pour la prochaine itération
      i = j;
    }
    
    //Mettre la capacité restante
    writeln();
    writeln("Capacité restantes : ", Q - sommeDemande);
    writeln("----------------------------------------");
  }
}
