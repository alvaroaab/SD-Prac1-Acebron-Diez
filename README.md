# SD-Prac1-Acebron-Diez
## Grup 
Pràctica 1 SD - Álvaro Acebrón i Marc Diez.
## Instal·lació
* Verificar els requeriments: Python3, ibm_boto3, awscli,  cloud-functions.
```
sudo apt-get install python3
pip3 install awscli --upgrade --user
pip install -U ibm-cos-sdk --upgrade --user
```
* Fer login a ibmcloud:
```
ibmcloud login -a cloud.ibm.com
ibmcloud plugin install cloud-functions
```
* Primer clonar el repositori: 
```
git clone https://github.com/alvaroaab/SD-Prac1-Acebron-Diez
```
* Afegir el fitxer ibm_cloud_config dins de la carpeta on s'ha clonat.
* Després, cal executar l'script prepare_cloud_files.sh per pujar les funcions al IBM Cloud Functions.
```
./prepare_cloud_files.sh
```
* Pujar l'arxiu que es vulgui analitzar a IBM COS pertinent.
* Executar l'Orchestrator i introduir els paràmetres correctament.
```
python3 orchestrator.py [nom_fitxer] [num_particions]
```
## Arquitectura i Implementació
### Orchestrator:
L'Orchestrator és la peça fonamental del MapReduce. S'encarrega de balancejar la càrrega de treball i invocar als map().
* 1r: Carrega la configuració introduïda per paràmetres i teclat.
* 2n: Aquest obté la mida del fitxer a analitzar.
* 3r: Executa tants map() com el número de particions. El map() és una funció que està al Cloud i se li passa per paràmetre com a diccionari tota la informació necessaria (Nom del fitxer, el rang que li toca,bucket name...). 
* 4t: S'utilitza la llibreria asyncio de python per a evitar fer una espera activa del resultat del map. Així pot fer totes les invocacions del map seguides.
* 5è: S'espera a què tots els map hagin acabat abans d'invocar el reduce().
* 6è: Un cop acabat el reduce(), si el resultat ha estat satisfactori descarrega el fitxer amb els resultats finals del COS.
* 7è: Mostra el resultat i el temps d'execució.
### Map:
* 1r: Obté la partició del fitxer corresponent.
* 2n: Depenen del programa indicat per l'usuari, executa el WordCount o el CountingWords de la partició.
* 3r: Puja l'arxiu dels resultats parcials al COS.
### Reduce:
* 1r: Obté els resultats parcials de les particions.
* 2n: Depenen del programa indicat per l'usuari, junta els resultats de la forma pertinent.
* 3r: Puja l'arxiu dels resultats finals al COS.
* 4t: Si tot ha estat correcte, retorna un "OK".
## Resultats
![Gràfiques](https://github.com/alvaroaab/SD-Prac1-Acebron-Diez/blob/master/results/Graphics.png)
![Gràfiques](https://github.com/alvaroaab/SD-Prac1-Acebron-Diez/blob/master/results/Speedup%20tables.png)
* No es pot analitzar un fitxer molt gran amb un número de particions petit. Això és degut a un overflow en el map() a l'hora d'obtenir l'arxiu del COS. També passa al reduce() si la mida del diccionari és massa gran.
* El resultat més òptim es dóna amb el número mínim de particions, sempre i quan no doni un error. 
* Si bé és cert que com més particions s'afegeixin, més paral·lelitzat estarà el programa, afegeix un cost a l'hora d'esperar a la finalització de tots els map(), quan es junten els resultats al reduce() i al fer la neteja dels fitxers.
