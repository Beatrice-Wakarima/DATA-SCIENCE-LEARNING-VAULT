### Project 1: Setting up a simple web server

In this project, you'll create a Docker container that runs a basic web server using Nginx. Nginx is one of the most popular open-source web servers for reverse proxying, load balancing, and more. By the end of this project, you will have learned how to create and run containers with Docker and expose ports so the application can be accessed from your local machine.

Difficulty level: Beginner

Technologies used: Docker, Nginx

#### Step-by-step instructions

- Install Docker: Make sure Docker is installed on your system.
- Create the project directory: Create a new folder and an `index.html` file inside it that will be served by Nginx.
- Write the Dockerfile: A Dockerfile is a script that defines the environment of the container. It tells Docker what base image to use, what files to include, and what ports to expose:

`FROM nginx:alpine COPY ./index.html /usr/share/nginx/html EXPOSE 80`

[Powered By](https://www.datacamp.com/datalab) 

- Build the Docker image: Navigate to your project folder and build the image using:

`docker build -t my-nginx-app .`

[Powered By](https://www.datacamp.com/datalab) 

- Run the container: Start the container and map port 80 of the container to port 8080 on your machine:

`docker run -d -p 8080:80 my-nginx-app`

[Powered By](https://www.datacamp.com/datalab) 

- Access the web server: Open your browser and navigate to http://localhost:8080 to see your created page.

### Project 2: Dockerizing a Python script

This project involves containerizing a simple Python script that processes data from a CSV file [using the pandas library](https://www.datacamp.com/courses/data-manipulation-with-pandas). The goal is to learn how to manage dependencies and execute Python scripts inside Docker containers, making the script portable and executable in any environment.

Difficulty level: Beginner

Technologies used: Docker, Python, pandas

#### Step-by-step instructions

- Write the Python script: Create a script named `process_data.py` that reads and processes a CSV file. Here’s an example script:

`import pandas as pd df = pd.read_csv('data.csv') print(df.describe())`

[Powered By](https://www.datacamp.com/datalab) 

- Create a `requirements.txt` file: This file lists the Python libraries the script needs. In this case, we only need `pandas`:

`pandas`

[Powered By](https://www.datacamp.com/datalab) 

- Write the Dockerfile: This file will define the environment for the Python script:

`FROM python:3.9-slim WORKDIR /app COPY requirements.txt . RUN pip install -r requirements.txt COPY . . CMD ["python", "process_data.py"]`

[Powered By](https://www.datacamp.com/datalab) 

- Build the Docker image:

`docker build -t python-script .`

[Powered By](https://www.datacamp.com/datalab) 

- Run the container:

`docker run -v $(pwd)/data:/app/data python-script`

[Powered By](https://www.datacamp.com/datalab) 

### Project 3: Building a simple multi-container application

This project will help you get familiar with Docker Compose by building a multi-container application. You’ll create a simple web application using Flask as the frontend and MySQL as the backend database. Docker Compose allows you to manage multiple containers that work together.

Difficulty level: Beginner

Technologies used: Docker, Docker Compose, Flask, MySQL

#### Step-by-step instructions

- Write the Flask application: Create a simple Flask app that connects to a MySQL database and displays a message. Here’s an example:

`from flask import Flask import mysql.connector   app = Flask(__name__)   def get_db_connection():  	connection = mysql.connector.connect( 	 host="db", 	 user="root", 	 password="example", 	 database="test_db"  	)  	return connection   @app.route('/') def hello_world():  	connection = get_db_connection()  	cursor = connection.cursor()  	cursor.execute("SELECT 'Hello, Docker!'")  	result = cursor.fetchone()  	connection.close()  	return str(result[0])   if __name__ == "__main__":  	app.run(host='0.0.0.0')`

[Powered By](https://www.datacamp.com/datalab) 

- Create the `docker-compose.yml` file: Docker Compose defines and runs multi-container Docker applications. In this file, you will define the Flask app and the MySQL database services:

`version: '3' services:   db:     image: mysql:5.7     environment:       MYSQL_ROOT_PASSWORD: example       MYSQL_DATABASE: test_db     ports:       - "3306:3306"     volumes:       - db_data:/var/lib/mysql    web:     build: .     ports:       - "5000:5000"     depends_on:       - db     environment:       FLASK_ENV: development     volumes:       - .:/app  volumes:   db_data:`

[Powered By](https://www.datacamp.com/datalab) 

- Write the Dockerfile for Flask: This will create the Docker image for the Flask application:

`FROM python:3.9-slim WORKDIR /app COPY requirements.txt . RUN pip install -r requirements.txt COPY . . CMD ["python", "app.py"]`

[Powered By](https://www.datacamp.com/datalab) 

- Build and run the containers: Use Docker Compose to bring up the entire application:

`docker-compose up --build`

[Powered By](https://www.datacamp.com/datalab) 

- **Access the Flask app:** Go to [http://localhost:5000](http://localhost:5000/) in your browser.

## Become a Data Engineer

Become a data engineer through advanced Python learning

## Intermediate-Level Docker Projects

The following projects are for those with a solid understanding of Docker basics. These will introduce more complex concepts, such as multi-stage builds and optimization techniques.

### Project 4: Multi-stage build for a Node.js application

Multi-stage builds help reduce Docker image sizes by separating the build and runtime environments. In this project, you will containerize a Node.js application using multi-stage builds.

Difficulty level: Intermediate

Technologies used: Docker, Node.js, Nginx

#### Step-by-step instructions

- Create a simple Node.js app: Write a basic Node.js server that returns a simple message. Here’s an example:

`const express = require('express'); const app = express();   app.get('/', (req, res) => res.send('Hello from Node.js'));   app.listen(3000, () => console.log('Server running on port 3000'));`

[Powered By](https://www.datacamp.com/datalab) 

- Write the Dockerfile with multi-stage build: The first stage builds the app, and the second stage runs the app with a lighter base image.

`# Stage 1: Build FROM node:14 as build-stage WORKDIR /app COPY package*.json ./ RUN npm install COPY . . # Add the following line if there's a build step for the app # RUN npm run build  # Stage 2: Run FROM node:14-slim WORKDIR /app COPY --from=build-stage /app . EXPOSE 3000 ENV NODE_ENV=production CMD ["node", "server.js"]`

[Powered By](https://www.datacamp.com/datalab) 

- Build the image:

`docker build -t node-multi-stage .`

[Powered By](https://www.datacamp.com/datalab) 

- Run the container:

`docker run -p 3000:3000 node-multi-stage`

[Powered By](https://www.datacamp.com/datalab) 

### Project 5: Dockerizing a machine learning model with TensorFlow

This project will involve containerizing a machine learning model using [TensorFlow](https://www.datacamp.com/courses/introduction-to-tensorflow-in-python). The goal is to create a portable environment where you can run TensorFlow models across various systems without worrying about the underlying setup.

Difficulty level: Intermediate

Technologies used: Docker, TensorFlow, Python

#### Step-by-step instructions

- Install TensorFlow in a Python script: Create a Python script `model.py` that loads and runs a pre-trained TensorFlow model:

`import tensorflow as tf model = tf.keras.applications.MobileNetV2(weights='imagenet') print("Model loaded successfully")`

[Powered By](https://www.datacamp.com/datalab) 

- Write the Dockerfile: Define the environment for TensorFlow inside Docker:

`FROM tensorflow/tensorflow:latest WORKDIR /app COPY . . CMD ["python", "model.py"]`

[Powered By](https://www.datacamp.com/datalab) 

- Build the image:

`docker build -t tensorflow-model .`

[Powered By](https://www.datacamp.com/datalab) 

- Run the container:

`docker run tensorflow-model`

[Powered By](https://www.datacamp.com/datalab) 

### Project 6: Creating a data science environment with Jupyter and Docker

This project focuses on creating a reproducible data science environment using Docker and [Jupyter notebooks](https://www.datacamp.com/tutorial/tutorial-jupyter-notebook). The environment will include popular Python libraries like pandas, [NumPy](https://www.datacamp.com/courses/introduction-to-numpy), and [scikit-learn](https://www.datacamp.com/courses/supervised-learning-with-scikit-learn).

Difficulty level: Intermediate

Technologies used: Docker, Jupyter, Python, scikit-learn

#### Step-by-step instructions

- Create the `docker-compose.yml` file: Define the Jupyter Notebook service and the necessary libraries. Here’s an example:

`version: '3' services:   jupyter:     	image: jupyter/scipy-notebook     	ports:     	- "8888:8888"     	volumes:     	- ./notebooks:/home/joelwembo/work`

[Powered By](https://www.datacamp.com/datalab) 

- Start the Jupyter Notebook: Use Docker Compose to start the Jupyter Notebook.

`docker-compose up`

[Powered By](https://www.datacamp.com/datalab) 

- Access the Jupyter Notebook: Open your browser and go to http://localhost:8888.

## Advanced-Level Docker Projects

These advanced-level projects will focus on real-world applications and advanced Docker concepts, such as deep learning pipelines and automated data pipelines.

### Project 7: Reducing a Docker image size for a Python application

In this project, you'll optimize a Docker image for a Python application by using minimal base images like Alpine Linux and implementing multi-stage builds to keep the image size as small as possible.

Difficulty level: Advanced

Technologies used: Docker, Python, Alpine Linux

#### Step-by-step instructions

- Write the Python script: Create a script that analyzes data using pandas. Here’s an example script:

`import pandas as pd df = pd.read_csv('data.csv') print(df.head())`

[Powered By](https://www.datacamp.com/datalab) 

- Optimize the Dockerfile: Use multi-stage builds and Alpine Linux to create a lightweight image.

`# Stage 1: Build stage FROM python:3.9-alpine as build-stage WORKDIR /app COPY requirements.txt . RUN pip install --no-cache-dir -r requirements.txt COPY script.py .  # Stage 2: Run stage FROM python:3.9-alpine WORKDIR /app COPY --from=build-stage /app/script.py . CMD ["python", "script.py"]`

[Powered By](https://www.datacamp.com/datalab) 

- Build the image:

`docker build -t optimized-python-app .`

[Powered By](https://www.datacamp.com/datalab) 

### Project 8: Dockerizing a deep learning pipeline with PyTorch

This project involves containerizing a deep learning pipeline using PyTorch. The focus is optimizing the Dockerfile for performance and size, making it easy to run deep learning models in different environments.

Difficulty level: Advanced

Technologies used: Docker, PyTorch, Python

#### Step-by-step instructions

- Install PyTorch in a Python script: Create a script that loads a pre-trained PyTorch model and performs inference. Here’s an example:

`import torch model = torch.hub.load('pytorch/vision', 'resnet18', pretrained=True) print("Model loaded successfully")`

[Powered By](https://www.datacamp.com/datalab) 

- Write the Dockerfile: Define the environment for PyTorch:

`FROM pytorch/pytorch:1.9.0-cuda11.1-cudnn8-runtime WORKDIR /app COPY requirements.txt . RUN pip install --no-cache-dir -r requirements.txt COPY model.py . CMD ["python", "model.py"]`

[Powered By](https://www.datacamp.com/datalab) 

- Build the image:

`docker build -t pytorch-model .`

[Powered By](https://www.datacamp.com/datalab) 

- Run the container:

`docker run pytorch-model` 

[Powered By](https://www.datacamp.com/datalab) 

### Project 9: Automating data pipelines with Apache Airflow and Docker

In this project, you’ll set up and containerize an [Apache Airflow](https://www.datacamp.com/courses/introduction-to-apache-airflow-in-python) environment to automate data pipelines. Apache Airflow is a popular tool for orchestrating complex workflows widely used in data engineering.

Difficulty level: Advanced

Technologies used: Docker, Apache Airflow, Python, PostgreSQL

#### Step-by-step instructions

- Create the `docker-compose.yml` file: Define the Airflow services and the PostgreSQL database:

`version: '3' services:   postgres:     image: postgres:latest     environment:       POSTGRES_USER: airflow       POSTGRES_PASSWORD: airflow       POSTGRES_DB: airflow     ports:       - "5432:5432"     volumes:       - postgres_data:/var/lib/postgresql/data    webserver:     image: apache/airflow:latest     environment:       AIRFLOW__CORE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow       AIRFLOW__CORE__EXECUTOR: LocalExecutor     depends_on:       - postgres     ports:       - "8080:8080"     volumes:       - ./dags:/opt/airflow/dags     command: ["webserver"]    scheduler:     image: apache/airflow:latest     environment:       AIRFLOW__CORE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow       AIRFLOW__CORE__EXECUTOR: LocalExecutor     depends_on:       - postgres       - webserver     volumes:       - ./dags:/opt/airflow/dags     command: ["scheduler"]  volumes:   postgres_data:`

[Powered By](https://www.datacamp.com/datalab) 

- Start the Airflow environment: Use Docker Compose to bring up the Airflow environment:

`docker-compose up`

[Powered By](https://www.datacamp.com/datalab) 

- Access the Airflow UI: Open your browser and go to [http://localhost:8080](http://localhost:8080/).

### Project 10: Deploying a data science API with FastAPI and Docker

Build and [deploy a data science API using FastAPI](https://www.datacamp.com/tutorial/introduction-fastapi-tutorial). You’ll containerize the API using Docker and focus on optimizing it for production environments.

Difficulty level: Advanced

Technologies used: Docker, FastAPI, Python, scikit-learn

#### Step-by-step instructions

- Write the FastAPI application: Create a simple API that uses a machine learning model for predictions. Here’s an example:

`from fastapi import FastAPI import pickle   app = FastAPI() with open("model.pkl", "rb") as f:    model = pickle.load(f)   @app.post("/predict/") def predict(data: list):    return {"prediction": model.predict(data)}`

[Powered By](https://www.datacamp.com/datalab) 

- Write the Dockerfile: Create a Dockerfile that defines the environment for FastAPI:

`FROM python:3.9-slim WORKDIR /app COPY requirements.txt . RUN pip install -r requirements.txt COPY . . CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]`

[Powered By](https://www.datacamp.com/datalab) 

- Build the image:

`docker build -t fastapi-app .`

[Powered By](https://www.datacamp.com/datalab) 

- Run the container:

`docker run -p 8000:8000 fastapi-app`

[Powered By](https://www.datacamp.com/datalab) 

## Tips for Working on Docker Projects

As you work through these projects, keep the following tips in mind:

- Start small: Begin with slightly challenging projects, then move on to more complex tasks. Building confidence with more straightforward tasks is critical.
- Document your progress: Keep a detailed log of your projects to track your learning and to use as a reference for future endeavors.
- Join Docker communities: Engage with online forums and local meetups to share your experiences, ask questions, and learn from others.
- Experiment and customize: Don't be afraid to tweak the projects, try different approaches, and explore new Docker features.
- Keep learning: Continue to expand your Docker knowledge by exploring advanced topics and tools such as [Kubernetes](https://www.datacamp.com/courses/introduction-to-kubernetes), Docker Swarm, or microservices architecture