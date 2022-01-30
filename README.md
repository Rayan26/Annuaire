# Student Book

pip install requirements.txt

#Dans un terminal :
cd backend
export FLASK_APP=backend
export FLASK_DEBUG=1
cd ..
flask run -p 5001

#Dans un autre terminal :
cd frontend
export FLASK_APP=frontend
export FLASK_DEBUG=1
cd ..
flask run -p 5000




#Pour la dockerisation (TODO)
# Fabriquer les réseaux Docker 
```angular2html
docker network create --gateway 192.168.20.1 --subnet 192.168.20.0/24 DMZ
docker network create --gateway 192.168.10.1 --subnet 192.168.10.0/24 BACK
docker network create --gateway 192.168.30.1 --subnet 192.168.30.0/24 DATA
```


# Fabriquer l'image
```
docker build -t docker-example .
```

# Démarrer le conteneur
```
docker run -p 127.0.0.1:5000:500/tcp -it docker-example
```


