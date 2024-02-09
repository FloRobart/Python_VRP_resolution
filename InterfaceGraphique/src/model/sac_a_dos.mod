/*********************************************
 * OPL 22.1.1.0 Model
 * Author: ra212336
 * Creation Date: 17 oct. 2023 at 14:45:39
 *********************************************/
int nbObjets=...;
range i=1..nbObjets;
int poidsObjets[i]=...;
int valeursObjets[i]=...;
int poidsMax=...;

dvar boolean x[i];

maximize sum(j in i) x[j]*valeursObjets[j];

subject to{
		sum(j in i) poidsObjets[j]*x[j] <= poidsMax;
}

execute{
	for ( var j in i ){
	  if (x[j]==1)
	  	write(poidsObjets[j] + " ");
	}	  		
}; 