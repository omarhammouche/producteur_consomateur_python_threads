#include<thread>
#include <iostream>
#include <fstream>
#include<vector>
#include <time.h>
#include <math.h>
#include<bits/stdc++.h>
#include<stdlib.h>
#include<mutex>

using namespace std::chrono; 
using namespace std;




int N ;
mutex myMutex;

int voiture(int depart,int N,int numVoiture, int **routes) {
	int  arrivee;
	int count = 0;
			arrivee = rand() % N;

	while(count < 5){ // 5 stops
		std::this_thread::sleep_for(std::chrono::milliseconds(800));

		cout << "voiture numero : " << numVoiture << "\n";
		if(myMutex.try_lock()){
			cout << depart << " -> " << routes[depart][arrivee] << "\n";
			depart = routes[depart][arrivee];
				
			cout << "\n";
			count++;
			arrivee = rand() % N;

		}
		else{
				//count++;
			myMutex.unlock();
			cout << "voiture " << numVoiture << " is waiting to go to " << routes[depart][arrivee] << "\n";
			cout << "cout = " << count << " voiture " << numVoiture << "\n";

	}
}
	return routes[depart][arrivee];
}


int main(int ac, char **av){ //int argc , char * args


// taille de la matrice
	N = atoi(av[1]);

	int nbrVoitures = N;

	cout << "le nombre de voiture : " << N  << endl;



int x=5,y=5;
// initialisation des tout les cases avec la valeur -1, matrice de taille fix de 5,15

int rows = N, cols = N;
int** routesVoitures = new int*[rows];
for (int i = 0; i < rows; ++i)
    routesVoitures[i] = new int[cols];

//int nbrRoutes;
int connectedNodes;
srand(time(NULL));

// remplissage des noeuds

for(int i =0;i<N;i++){
//nbrRoutes = rand() % N+1;
for(int j =0;j<N;j++){
// recherhcer si le noeus actuelle ne point pas vers lui même

connectedNodes = rand() % N; // elle peut generer le même nombre plusieurs fois
// mais c pas grave ça pose pas un problème dans la logique

// pour éviter que le noeud point sur lui même avant de l'ajouter
if(connectedNodes != i)// 
routesVoitures[i][j] = connectedNodes;
else
	j--;
}
}

// création des threads / voitures
std::vector<thread> mesVoitures;
int newNode;

for(int i=0;i<nbrVoitures;i++){ // N c'est le nombre de station et N - x est le nombre de voiture
	newNode = rand() % N;
	mesVoitures.push_back(std::thread(voiture,i,N,i+1, routesVoitures));
}

for(int i=0;i<nbrVoitures;i++) mesVoitures[i].join();

	cout << "the end" << endl;

// parcours des voitures


// affichge
/*
for(int i=0;i<N;i++){
	for(int j=0;j<N;j++){
		if(routesVoitures[i][j] != -1){
			cout << routesVoitures[i][j] << " ";
		}
		else 
			cout << " ";
	}

	cout << "\n";
}*/
}

