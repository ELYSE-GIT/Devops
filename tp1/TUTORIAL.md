# RASOLOARIVONY ELYSE - M1 BDIA APP - EFREI
##### My pseudo: RASEL
Objectifs à atteindre TP1 :

* Création d'un repository Github 
* Création d'un wrapper qui retourne la météo d'un lieu donné avec sa latitude et sa longitude (passées en variable d'environnement) en utilisant openweather API dans le langage deprogrammation de votre choix (bash, python, go, nodejs, etc)
* Packager son code dans une image Docker
* Mettre à disposition son image sur DockerHub
* Mettre à disposition son code dans un repository Github

---

#### Mes comptes et sources utilisés

* github: https://github.com/ELYSE-GIT/Devops
* Clé API openweathermap : https://home.openweathermap.org/api_keys
* dockerhub : https://hub.docker.com/repository/docker/rasel5586/tp1-devops
---

#### Solutions utilisées :
- Linux (ubuntu) 
- environnement virtuel (développement en local)
- Python 
- requirements.txt (packages python avec leurs versions)
- Docker

---

## ETAPES 

#### Activation d'un environnement virtuel:
```bash
$ python -m venv venv
$ source venv/bin/activate
```
#### Obtention de ma clé privée et profiter de l'API **openweathermap**
* mettre ma clé dans la variable d'environnement *APIKEY*
``` bash
$ export APIKEY=c1865064c90221bae21160f13bcd0d7d
```

* Tester l'api avec ma clé
```
(venv) rasel@rasel:~/Desktop/Devops/tp/tp1/tp1Correction$ curl "http://api.openweathermap.org/data/2.5/weather?q=palermo&appid=$APIKEY"

{"coord":{"lon":13.5833,"lat":37.8167},"weather":[{"id":801,"main":"Clouds","description":"few clouds","icon":"02d"}],"base":"stations","main":{"temp":301.24,"feels_like":300.36,"temp_min":296.34,"temp_max":303.6,"pressure":1017,"humidity":31,"sea_level":1017,"grnd_level":957},"visibility":10000,"wind":{"speed":1.36,"deg":330,"gust":1.59},"clouds":{"all":18},"dt":1654450682,"sys":{"type":2,"id":2007649
```

#### Utilisation de l'API openweather sous python
* Création d'un script *Curl.py*
```bash
$ cat > Curl.py

```

```python
import  requests
import  os

APIKEY = os.environ['APIKEY'] # lecture de la variable d'environnement

response = requests.get("http://api.openweathermap.org/data/2.5/weather?q=monaco&appid="+APIKEY)

print(response.status_code)
print(response.json())
````

```bash 
python Curl.py

{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 298.08, 'feels_like': 298.8, 'temp_min': 296.03, 'temp_max': 301.56, 'pressure': 1015, 'humidity': 83}, 'visibility': 10000, 'wind': {'speed': 1.54, 'deg': 140}, 'clouds': {'all': 0}, 'dt': 1654423514, 'sys': {'type': 2, 'id': 2006345, 'country': 'MC', 'sunrise': 1654400996, 'sunset': 1654456078}, 'timezone': 7200, 'id': 2993457, 'name': 'Monaco', 'cod': 200}
```

* Mettre dans un fichier *requirements.txt* toutes les dépendances
```bash
$ cat > requirements.txt
flask==2.1.2
requests==2.22.0
click==8.1.3
importlib-metadata==4.11.4
itsdangerous==2.1.2
Jinja2==3.1.2
MarkupSafe==2.1.1
Werkzeug==2.1.2
zipp==3.8.0
python-dotenv
```


# Utilisation de Docker:

* Création du fichier **Dockerfile**:

```bash
$ cat > Dockerfile

FROM python:3.8.13-alpine3.15 #image de base

WORKDIR /tp1 # répertoire de travail dans l'image

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY Curl.py . 

EXPOSE 5000 # numéro de port utilisé

ENTRYPOINT [ "python", "Curl.py" ]

```

* Construction de l'**image docker** que je vais tagger *imagetp1.0.1*:
```bash
(venv) rasel@rasel:~/Desktop/Devops/tp/tp1/tp1Correction$ docker build . --tag imagetp1.0.1

Sending build context to Docker daemon  14.27MB
Step 1/7 : FROM python:3.8.13-alpine3.15
 ---> 594d7750c885
Step 2/7 : WORKDIR /tp1
 ---> Using cache
 ---> 0650e9824905
Step 3/7 : COPY requirements.txt .
 ---> Using cache
 ---> ae1a696cadce
Step 4/7 : RUN pip3 install -r requirements.txt
 ---> Using cache
 ---> 66ef736f8fba
Step 5/7 : COPY Curl.py .
 ---> Using cache
 ---> fc2f34ae4045
Step 6/7 : EXPOSE 5000
 ---> Using cache
 ---> 6a1b3545726e
Step 7/7 : ENTRYPOINT [ "python", "Curl.py" ]
 ---> Using cache
 ---> b71e37b07d8f
Successfully built b71e37b07d8f
Successfully tagged imagetp1.0.1:latest

```

* Exécution du conteneur
```bash
(venv) rasel@rasel:~/Desktop/Devops/tp/tp1/tp1Correction$ docker run -p 5000:5000 --env APIKEY=$APIKEY --rm imagetp1.0.1
200
{'coord': {'lon': 7.419, 'lat': 43.7314}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 294.66, 'feels_like': 295.09, 'temp_min': 293.93, 'temp_max': 303.02, 'pressure': 1012, 'humidity': 85}, 'visibility': 10000, 'wind': {'speed': 2.57, 'deg': 60}, 'clouds': {'all': 0}, 'dt': 1654459662, 'sys': {'type': 2, 'id': 2006345, 'country': 'MC', 'sunrise': 1654400996, 'sunset': 1654456078}, 'timezone': 7200, 'id': 2993457, 'name': 'Monaco', 'cod': 200}

```

---

### Docker : exposer l'api de façon plus générale

* Modification du script *Curl.py*
``` python
import  requests
import  os

# affectation des variables d'environnements dans des variables python

api_key = os.environ['APIKEY'] 
lat = os.environ['LAT']
lon = os.environ['LONG']


url = "https://api.openweathermap.org/data/2.5/weather?lat="+lat+"&lon="+lon+"appid="+api_key

response = requests.get(url)

print(response.status_code)
print(response.json())
```

* Reconstruction de l'image:
````bash
(venv) rasel@rasel:~/Desktop/Devops/tp/tp1/tp1Correction$ docker build . --tag imagetp1.0.1
Sending build context to Docker daemon  14.28MB
Step 1/7 : FROM python:3.8.13-alpine3.15
 ---> 594d7750c885
Step 2/7 : WORKDIR /tp1
 ---> Using cache
 ---> 0650e9824905
Step 3/7 : COPY requirements.txt .
 ---> Using cache
 ---> ae1a696cadce
Step 4/7 : RUN pip3 install -r requirements.txt
 ---> Using cache
 ---> 66ef736f8fba
Step 5/7 : COPY Curl.py .
 ---> c613cda426e0
Step 6/7 : EXPOSE 5000
 ---> Running in 100c27a227a6
Removing intermediate container 100c27a227a6
 ---> b80e5d6c46fe
Step 7/7 : ENTRYPOINT [ "python", "Curl.py" ]
 ---> Running in d4c517d519ee
Removing intermediate container d4c517d519ee
 ---> dc0a665f7da5
Successfully built dc0a665f7da5
Successfully tagged imagetp1.0.1:latest

````

* Exécution du conteneur avec l'image *imagetp1.0.1* modifiée. 

*Information sur la postion de la Tour EIffel :*
```bash
(venv) rasel@rasel:~/Desktop/Devops/tp/tp1/tp1Correction$ docker run --env LAT="48.858370" --env LONG="2.294481" --env APIKEY=$APIKEY --rm imagetp1.0.1
200
{'coord': {'lon': 2.2931, 'lat': 48.8596}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 290.39, 'feels_like': 290.36, 'temp_min': 288.6, 'temp_max': 291.49, 'pressure': 1017, 'humidity': 84}, 'visibility': 10000, 'wind': {'speed': 3.6, 'deg': 290}, 'clouds': {'all': 75}, 'dt': 1654461646, 'sys': {'type': 2, 'id': 2012208, 'country': 'FR', 'sunrise': 1654400984, 'sunset': 1654458550}, 'timezone': 7200, 'id': 2990611, 'name': 'Neuilly-sur-Seine', 'cod': 200}
```

* Voir les images construites antérieurement disponibles dans mon local:

```bash 
(venv) rasel@rasel:~/Desktop/Devops/tp/tp1/tp1Correction$ docker images
REPOSITORY             TAG                 IMAGE ID       CREATED          SIZE
imagetp1.0.1           latest              8b2b2741e854   2 minutes ago    61.5MB
<none>                 <none>              677833091be3   4 minutes ago    61.5MB
<none>                 <none>              917ebff99f57   6 minutes ago    61.5MB
...
```
NB : Sauvegardons dans un coin de notre tête l'*IMAGE ID* de imagetp1.0.1, nous allons l'utiliser pour publier sur un Docker Hub

#### Utilisation du **REGISTRY**
Dans notre cas, nous allons prendre l'exemple de **Docker Hub**. Notre but ici est de publier l'image *imagetp1.0.1* construite en local sur un repository publique 

NB : le lien est indiqué au dessus de la page

* Connection à mon compte Docker hub 
```bash
(venv) rasel@rasel:~/Desktop/Devops/tp/tp1/tp1Correction$ docker login -u rasel5586
Password: 
WARNING! Your password will be stored unencrypted in /home/rasel/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded

``` 

* Re-tager l'image avant sa publication (on peut également utiliser l'IMAGE ID : 8b2b2741e854)
```
docker tag imagetp1.0.1 rasel5586/tp1-devops:imagetp1.0.1

```

* Envoie de l'image sur mon repository publiques : https://hub.docker.com/repository/docker/rasel5586/tp1-devops
```bash
(venv) rasel@rasel:~/Desktop/Devops/tp/tp1/tp1Correction$ docker push rasel5586/tp1-devops:imagetp1.0.1
The push refers to repository [docker.io/rasel5586/tp1-devops]
62a634910e5f: Pushed 
d951dd8e2f91: Pushed 
606c2d85c5b0: Pushed 
b7eb013979b5: Pushed 
6b5c9e1a7f84: Layer already exists 
f1859b30ca6b: Layer already exists 
6a35d52a66fd: Layer already exists 
fbd7d5451c69: Layer already exists 
4fc242d58285: Layer already exists 
imagetp1.0.1: digest: sha256:635fa1705907fbb5d31dd211555c416e3f0424fe5f63447edb193decfc8a2945 size: 2200

```

####  Utilisation de mon image via mon repository public sur docker Hub 
```bash
(venv) rasel@rasel:~/Desktop/Devops/tp/tp1/tp1Correction$ docker run --env LAT="48.858370" --env LONG="2.294481" --env APIKEY=$APIKEY --rm rasel5586/tp1-devops:imagetp1.0.1
200
{'coord': {'lon': 2.2945, 'lat': 48.8584}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 290, 'feels_like': 289.99, 'temp_min': 287.99, 'temp_max': 290.99, 'pressure': 1017, 'humidity': 86}, 'visibility': 10000, 'wind': {'speed': 2.57, 'deg': 290}, 'clouds': {'all': 0}, 'dt': 1654463942, 'sys': {'type': 2, 'id': 2012208, 'country': 'FR', 'sunrise': 1654400984, 'sunset': 1654458549}, 'timezone': 7200, 'id': 6545270, 'name': 'Palais-Royal', 'cod': 200}
```


Remarques : 
- N'oubliez pas d'exporter votre clé personnel avant d'exécuter
```export APIKEY=*****``` 
```
docker run --env LAT="48.858370" --env LONG="2.294481" --env APIKEY=$APIKEY --rm rasel5586/tp1-devops:imagetp1.0.1
```

- Lors de la création du script.py, l'url doit être directement intégré dans requests.get() et non par l'intérmédiaire d'une variable url.
- Dans le fichier requirements, il y des packages qui ne sont pas nécessaires mais j'utiliserais personellement plus tard
