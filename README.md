# sensor-watcher-api
 
sensor-watcher-api is a REST API project to calculate the difference between moving averages of two periods of sensor values. The project uses MongoDB as the database solution to retrieve data.

#### Core dependencies
  - Python 3.7.3
  - Flask
  - MongoDB

### Sample Data
- 


###  How to install and run?
You can install the project with or without docker. Make your choice.
- If you don't want to install it with docker, you can choose the first option. This option assumes that you have already installed mongodb on your system.
- If you want to install it with docker and you already have MongoDB on your system, you can choose the second option.
- If you want to install it with docker and you **don't** have Mongodb on your system, you can choose the third option.
- The flask app reads config values from environment variables. Right now in the project, there is only one config value needed and it is MongoDb connection string. We tell below in every section how you can set this value to enable the flask app connect to mongodb properly.


#### 1. Install and run without docker
**Note:** This step assumes you have alrady installed MongoDB on your system.
- Firstly, create a virtual environment outside project's folder and install dependencies.
 ```sh
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ cd sensor-watcher-api/
$ pip install -r requirements.txt
```

- The project reads the configurations from environment variables.You have to set the MongoDB connection string as:
 ```sh
$ export MONGODB_CONN_STR=mongodb://localhost:27017/sensors
```
- In the project's top folder run the project with gunicorn http server.
 ```sh
$ gunicorn run:app -b 0.0.0.0:8080
```
Now the flask app is serving on **0.0.0.0:8080**

- You have to insert the sample data into mongodb because the endpoints retrieve the required data from mongodb to make the calculations. I created a script called **sync_data_to_mongo.py** that makes this job. This script reads the sample data files that are in **src/scripts/data** folder, preprocesses them, inserts the data  into MongoDB and sets the required database indexes. Run this script as:
 ```sh
$ cd src/scripts
$ python sync_data_to_mongo.py
```

#### 2. Install and run with docker build
**Note:** This step assumes you have already installed MongoDB on your system.
 - Move to the project's top folder and build the image with this command:

```sh
$ docker build -t sensor-watcher-image .
```
 - Then run the container with this command and the flask app will be serving on **0.0.0.0:8080**
```sh
$ docker run --name sensor-watcher-container --env MONGODB_CONN_STR='mongodb://host.docker.internal:27017/sensors' -d -p 8080:8080 sensor-watcher-image
```
**Note:** When you specify mongodb host as **host.docker.internal** you basically tell the container to look for mongodb outside the container within the same host.

- Right now the only thing left for this choice of installation is inserting the sample data into MongoDB if you haven't done yet. We are going to run the **sync_data_to_mongo.py** script inside our **sensor-watcher-container** we just created.
```sh
$ docker exec -it sensor-watcher-container /bin/bash
$ cd src/scripts
$ python sync_data_to_mongo.py
```
#### 3. Install and run with docker compose
**Note:** If you currently don't have MongoDB on your system, this option is suitable for you. You can install MongoDB along with the flask application by using docker-compose.
 - Move to the project's top folder and run this command and the flask app and mongodb containers will run

```sh
$ docker-compose up -d
```
- Since MongoDB container is also running in our computer now, we can insert the sample data in our db. We are going to run the **sync_data_to_mongo.py** script inside our **sensor-watcher-container** we just created.
```sh
$ docker exec -it sensor-watcher-container /bin/bash
$ cd src/scripts
$ python sync_data_to_mongo.py
```