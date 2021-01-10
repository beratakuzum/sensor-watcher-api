# sensor-watcher-api
 
sensor-watcher-api is a REST API project to calculate the difference between moving averages of sensor values of two different periods. The project uses MongoDB as the database solution to retrieve data.

### Core dependencies
  - Python 3.7
  - Flask
  - MongoDB

### Sample Data
- In **src/scripts/data** folder, there are 4 files that include sample data to use for calculating moving average.
We need to insert sample data into MongoDB so that our endpoints can reach them. In order to insert the sample data into mongodb, you need to run the  **sync_data_to_mongo.py** script.
This script reads the sample data files that are in **src/scripts/data** folder, preprocesses them, inserts the data into MongoDB and sets the required database indexes.
We tell below in the next sections how you can run this script.

##  How to install and run?
You can install the project with or without docker. Make your choice.
- If you don't want to install it with docker, you can choose the first option. This option assumes that you have already installed mongodb on your system.
- If you want to install it with docker and you already have MongoDB on your system, you can choose the second option.
- If you want to install it with docker and you **don't** have Mongodb on your system, you can choose the third option.
- The flask app reads config values from environment variables. Right now in the project, there is only one config value needed and it is MongoDb connection string. We tell below in every section respectively 
how you can set this value to enable the flask app connect to mongodb properly.


#### 1. Install and run without docker
**Note:** This step assumes you have alrady installed MongoDB on your system.
- Firstly, create a virtual environment outside the project's folder and install the dependencies.
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
- In the project's folder, run the project:
 ```sh
$ python run.py
```
Now the flask app is serving on **http//:0.0.0.0:8080**

- In order to insert the sample data into mongodb, you need to run the  **sync_data_to_mongo.py** script. Run this script as:
 ```sh
$ cd src/scripts
$ python sync_data_to_mongo.py
```

#### 2. Install and run with docker build
**Note:** This step assumes you have already installed MongoDB on your system.
 - Move to the project's folder and build the image with this command:

```sh
$ docker build -t sensor-watcher-image .
```
 - Then run the container with this command and the flask app will be serving on **http://0.0.0.0:8080**
```sh
$ docker run --name sensor-watcher-container --env MONGODB_CONN_STR='mongodb://172.17.0.1:27017/sensors' -d -p 8080:8080 sensor-watcher-image
```
**Note:** When you specify mongodb host as **172.17.0.1** as we did above in the command, 
you basically tell the container to look for mongodb outside the container within the same host.

- Right now the only thing left for this choice of installation is inserting the sample data into MongoDB if you haven't done it yet. We are going to run the **sync_data_to_mongo.py** script inside our **sensor-watcher-container** we just created.
```sh
$ docker exec -it sensor-watcher-container /bin/bash
$ cd src/scripts
$ python sync_data_to_mongo.py
```
#### 3. Install and run with docker compose
**Note:** If you currently don't have MongoDB on your system, this option is suitable for you. You can install MongoDB along with the flask application by using docker-compose.
 - Move to the project's folder and run this command and the flask app and mongodb containers will run.

```sh
$ docker-compose up -d
```
- The flask app is serving on **http://0.0.0.0:8080**
- Since MongoDB container is also running in our computer now, we can insert the sample data in into our db. 
We are going to run the **sync_data_to_mongo.py** script inside our **sensor-watcher-container** we just created.
```sh
$ docker exec -it sensor-watcher-container /bin/bash
$ cd src/scripts
$ python sync_data_to_mongo.py
```
##  How to run the tests?
- Some of the integration tests requires the sample data to be inserted into MongoDB. After making sure you have the sample data in MongoDB, you can just run this command inside the project's folder to run the tests: 
```sh
$ pytest
```
**Note:** If you installed the project with docker, you have to run this command inside the container as: 

```sh
$ docker exec -it sensor-watcher-container /bin/bash
$ pytest
```