# Selal 🧺 : A Product Content-Based Recommender Systems to upsize baskets in online stores

## To run the app

```shell-session
docker build -t app:latest ./app
docker network create mynetwork
docker run --rm --network=mynetwork -p 8000:8000 app:latest
```

## To carry out the stress testing

```shell-session
docker build -t locust:latest ./locust
docker run --rm --network=mynetwork -p 8089:8089 locust:latest
```