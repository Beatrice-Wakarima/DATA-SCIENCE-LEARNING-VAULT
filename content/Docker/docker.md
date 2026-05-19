- **Container Orchestration**: Understanding the basics and tools of container orchestration, crucial for deploying and managing containerized applications​​.
- **Docker Swarm and Kubernetes**: Knowledge of these two popular container orchestration tools is required, with Docker Swarm being user-friendly and Kubernetes ideal for complex, high-demand applications​​.
- **Image Creation, Registry, and Management**: Learning to handle Docker images, which are snapshots of a container, forms a significant part of the curriculum​​.
- **Installation and Configuration**: Mastery in installing and configuring Docker, a skill regularly needed in practical scenarios​​.
- **Security & Networking**: Understanding Docker’s networking features and prioritizing security is essential​​.
- **Storage and Volumes:** Knowledge of Docker volumes, which store information, is critical​​.
- **Docker Enterprise Edition**: Familiarity with Docker EE, designed for critical deployments, enhances one's skill set​​.
### Docker images

Docker images are the fundamental building blocks of containers. They are immutable, read-only templates containing everything needed to run an application, including the operating system, application code, runtime, and dependencies.

Images are built using a `Dockerfile`, which defines the instructions for creating an image layer by layer.

Images can be stored in and retrieved from container registries such as Docker Hub.

Here are some example commands for working with images:

- `docker pull nginx`: Fetch the latest Nginx image from Docker Hub.
- `docker images`: List all available images on the local machine.
- `docker rmi nginx`: Remove an image from the local machine.

### Docker containers

A Docker container is a running instance of a Docker image. Containers provide an isolated runtime environment where applications can run without interfering with each other or the host system.Each container has its own filesystem, networking, and process space but shares the host kernel.

Containers follow a simple lifecycle involving creation, starting, stopping, and deletion. Here’s a breakdown of common container management commands:

1. Creating a container: `docker create` or `docker run`
2. Starting a container: `docker start`
3. Stopping a container: `docker stop`
4. Restarting a container: `docker restart`
5. Deleting a container: `docker rm`

Let’s see a practical example. The following command runs an Nginx container in detached mode (running in the background), mapping port 80 inside the container to port 8080 on the host machine:

`docker run -d -p 8080:80 nginx`

[](https://app.datacamp.com/workspace)

After running this command, Docker will pull the Nginx image (if not already available), create a container, and start it.

To check all running and stopped containers:

`docker ps -a`

[](https://app.datacamp.com/workspace)

This will display a list of all containers and details like their status and assigned ports.

### Docker Hub

[Docker Hub](https://hub.docker.com/) is a cloud-based registry service for finding, storing, and distributing container images. Users can push custom images to Docker Hub and share them publicly or privately.

Here are some commands for interacting with Docker Hub:

- `docker login`: Authenticate with Docker Hub.
- `docker push my-image`: Upload a custom-built image to Docker Hub.
- `docker search ubuntu`: Search for official and community images.
- `docker pull ubuntu`: Download an Ubuntu image from Docker Hub.

New to containerization? Get a solid foundation with [the Containerization and Virtualization Concepts](https://www.datacamp.com/courses/containerization-and-virtualization-concepts) course.

## Running Your First Docker Container

Now that we’ve covered Docker's core concepts, it’s time to put them into action! Let’s start by running our first container to ensure Docker is installed correctly and working as expected.

To test your Docker installation, open PowerShell (Windows) or Terminal (Mac and Linux) and run:

`docker run hello-world`

[](https://app.datacamp.com/workspace)

This pulls the `hello-world` image from DockerHub and runs it in a container.

![Docker hello-world image example](https://media.datacamp.com/cms/ad_4nxdf3-dz6hl2eytum-s5_zqnstaxhnyidybkjyjf1_fdje05jcfs-za-y5ezco2xybkzybpxa-d2o3fi7arejf4wd-l65jkt3upip0ts7nnozcgofopz9dk7yiuvx5lb_tgr-gig.png)

Docker hello-world image example

Now, let’s go a step further and run a real-world application—an Nginx web server. Execute the following command:

`docker run -d -p 8080:80 nginx`

[](https://app.datacamp.com/workspace)

The above command does the following:

- The `-d` flag runs the container in detached mode, meaning it runs in the background.
- The `-p 8080:80` flag maps port 80 inside the container to port 8080 on your local machine, allowing you to access the web server.

Once the command runs successfully, open a browser and visit: `http://localhost:8080`

![Accessing web server at localhost:8080](https://media.datacamp.com/cms/ad_4nxe-1us6lcvjvr75eyx1mt1svm4hnhlxxdpiehedvbb-3clxibm4teey5e5da32abefikmdiuzwhmewflbkvpdnlzr5l30e0zg25gxs6nmezfkbcxi4qnm0uopfed46li-tkd376qw.png)

Accessing web server at localhost:8080

You should see the default Nginx welcome page, confirming that your web server is running inside a container!

You will also see a container running in your Docker Desktop:

![Nginx container running on port 8080](https://media.datacamp.com/cms/ad_4nxfnzxsaap2i8spv2f6_mv1ffhkefgstbmj7h6tusxdz2o_9ofpiqw0jam7lbpfk7pxqux8ohbvhb4mimuxs-z9il2typvmmgh9al-r-ivplan2fkdy89obxbstejs9ejmuyxjuulg.png)

Nginx container running on port 8080

## Building Your First Docker Image

So far, we’ve been running pre-built images from Docker Hub. But what if you need a custom environment tailored to your application? That’s where building your own Docker image comes in.

Creating a Docker image involves writing a `Dockerfile`, a script that automates image-building. This ensures consistency and portability across different environments. Once an image is built, it can be run as a container to execute applications in an isolated environment. 

In this section, we’ll learn the fundamentals of writing a Dockerfile, building a custom image, and running it as a container.

### Dockerfile basics

A `Dockerfile` is a script containing a series of instructions that define how a Docker image is built. It automates the image creation process, ensuring consistency across environments. Each instruction in a `Dockerfile` creates a new layer in the image. Here’s a breakdown of an example Dockerfile for a simple Python Flask app:

`# Base image containing Python runtime FROM python:3.9  # Set the working directory inside the container WORKDIR /app  # Copy the application files from the host to the container COPY . /app  # Install the dependencies listed in requirements.txt RUN pip install -r requirements.txt  # Define the command to run the Flask app when the container starts CMD ["python", "app.py"]`

[](https://app.datacamp.com/workspace)

This code snippet is a Dockerfile, which is used to create a Docker image for a Python application, specifically a Flask app.
• Here's a breakdown: **FROM python:3.9**: This line specifies the base image, which includes Python 3.9.
• It provides the Python runtime environment needed for the app.
• **WORKDIR /app**: Sets the working directory inside the container to **/app**.
• This is where subsequent commands will be executed.
• **COPY .
• /app**: Copies all the files from the current directory on the host machine to the **/app** directory in the container.
• **RUN pip install -r requirements.txt**: Installs the Python dependencies listed in **requirements.txt** using pip.
• This ensures all necessary packages are available in the container.
• **CMD ["python", "app.py"]**: Defines the command to run the Flask app.
• When the container starts, it will execute **python app.py**, launching the application.
• Overall, this Dockerfile sets up a container environment to run a Python Flask application, handling dependencies and defining the startup command.

Was the AI assistant helpful? Yes No

In the above command:

- `-v my-volume:/app/data` mounts the `my-volume` storage to the `/app/data` directory inside the container.
- Any data stored in `/app/data` will persist even if the container stops or is removed.

Breaking down the Dockerfile above:

- `FROM python:3.9`: Specifies the base image with Python 3.9 pre-installed.
- `WORKDIR /app`: Sets `/app` as the working directory inside the container.
- `COPY . /app`: Copies all files from the host’s current directory to `/app` in the container.
- `RUN pip install -r requirements.txt`: Installs all required dependencies inside the container.
- `CMD ["python", "app.py"]`: Defines the command to execute when the container starts.

### Building and running the image

Once the Dockerfile is defined, you can build and run the image using the following commands:

#### Step 1: Build the image

`docker build -t my-flask-app .`

[](https://app.datacamp.com/workspace)

The code snippet **docker build -t my-flask-app .** is a Docker command used to create a Docker image from a Dockerfile located in the current directory (denoted by the dot **.** at the end).
• Here's a breakdown: **docker build**: This command initiates the process of building a Docker image.
• **-t my-flask-app**: The **-t** flag tags the image with a name, in this case, **my-flask-app**.
• This makes it easier to reference and manage the image later.
• **.**: This specifies the build context, which is the current directory.
• Docker will look for a Dockerfile here to build the image.
• Overall, this command creates a Docker image named **my-flask-app** using the instructions in the Dockerfile found in the current directory.

Was the AI assistant helpful? Yes No

The above command:

- Uses the current directory (`.`) as the build context.
- Reads the `Dockerfile` and executes its instructions.
- Tags (`-t`) the resulting image as `my-flask-app`.

#### Step 2: Run the image as a container

`docker run -d -p 5000:5000 my-flask-app`

[](https://app.datacamp.com/workspace)

The above command:

- Runs the container in detached mode (`-d`).
- Maps port 5000 inside the container to port 5000 on the host (`-p 5000:5000`).

Once running, you can access the Flask application by navigating to `http://localhost:5000` in a browser.

## Docker Volumes and Persistence

By default, data inside a Docker container is temporary—once the container stops or is removed, the data disappears. To persist data across container restarts and share it between multiple containers, Docker provides volumes, a built-in mechanism for managing persistent storage efficiently.

Unlike storing data inside the container’s filesystem, volumes are managed separately by Docker, making them more efficient, flexible, and easier to back up.

In the next section, we’ll explore how to create and use Docker volumes to ensure data persistence in your containers.

### Creating and using Docker volumes

#### Step 1: Create a volume

Before using a volume, we need to create one. Run the following command:

`docker volume create my-volume`

[](https://app.datacamp.com/workspace)

This creates a named volume called `my-volume`, which Docker will manage separately from any specific container.Step 2: Use the volume in a container

Now, let's start a container and mount the volume inside it:

`docker run -d -v my-volume:/app/data my-app`

[](https://app.datacamp.com/workspace)

In the above command:

- `-v my-volume:/app/data` mounts the `my-volume` storage to the `/app/data` directory inside the container.
- Any data stored in `/app/data` will persist even if the container stops or is removed.

## Docker Compose for Multi-Container Applications

So far, we’ve been working with single-container applications, but many real-world applications require multiple containers to work together. For example, a web application might need a backend server, a database, and a caching layer—each running in its own container. Managing these containers manually with separate `docker run` commands can quickly become tedious.

That’s where Docker Compose comes in.

### What is Docker Compose?

Docker Compose is a tool that simplifies the management of multi-container applications. Instead of running multiple `docker run` commands, you can define an entire application stack using a `docker-compose.yml` file and deploy it with a single command.

### Writing a Docker Compose file

Now, let’s create a real-world example—a simple Node.js application that connects to a [MongoDB database](https://www.datacamp.com/courses/introduction-to-using-mongodb-for-data-science-with-python). Instead of managing the two containers separately, we’ll define them in a `docker-compose.yml` file.

Here’s how we define our multi-container setup in Docker Compose:

`version: '3' services:   web:     build: .     ports:       - "3000:3000"     depends_on:       - database   database:     image: mongo     volumes:       - db-data:/data/db volumes:   db-data:`

[](https://app.datacamp.com/workspace)

This code snippet is a Docker Compose file, which is used to define and run multi-container Docker applications.
• **version: '3'**: Specifies the version of the Docker Compose file format being used.
• **services**: Defines the services that make up the application.
• - **web**: This service is for the web application.
• - **build: .**: Builds the Docker image for the web service using the Dockerfile in the current directory.
• - **ports**: Maps port 3000 on the host to port 3000 in the container, allowing access to the web application.
• - **depends_on**: Specifies that the web service depends on the database service, ensuring the database starts before the web service.
• - **database**: This service uses a MongoDB image.
• - **image: mongo**: Uses the official MongoDB Docker image.
• - **volumes**: Mounts a named volume **db-data** to **/data/db** inside the container, which is where MongoDB stores its data.
• **volumes**: Defines named volumes for persistent data storage.
• - **db-data**: A named volume used by the database service to persist data across container restarts.
• Overall, this setup aims to run a web application that depends on a MongoDB database, with data persistence ensured through a named volume.

Was the AI assistant helpful? Yes No

Breaking down the file above:

- `version: '3'`: Specifies the Docker Compose version.
- `services:`: Defines individual services (containers).
- `web:`: Defines the Node.js web application.
- `database:`: Defines the MongoDB database container.
- `volumes:`: Creates a named volume (`db-data`) for MongoDB data persistence.

### Running multi-container applications

Once the `docker-compose.yml` file is ready, we can launch the entire application stack with a single command:

`docker-compose up -d`

[](https://app.datacamp.com/workspace)

The previous command starts both the web and database containers in detached mode (`-d`).

To stop all services, use:

`docker-compose down`

[](https://app.datacamp.com/workspace)

This stops and removes all containers while preserving volumes and network settings.

## Docker Networking Basics

So far, we’ve focused on running containers and managing storage, but what happens when containers need to communicate with each other? In most real-world applications, containers don’t operate in isolation—they need to exchange data, whether a web server talks to a database or microservices interact with each other.

Docker provides a range of networking options to accommodate different use cases, from isolated internal networks to externally accessible configurations.

Ready to level up your Docker skills? Enroll in [Intermediate Docker](https://www.datacamp.com/courses/intermediate-docker) to explore multi-stage builds, advanced networking, and more!

### What is Docker networking?

Docker networking is a built-in feature that allows containers to communicate with each other, whether on the same host or across multiple hosts in a distributed environment. It provides network isolation, segmentation, and connectivity options suited for different deployment scenarios.

Docker supports multiple network types, each serving different use cases:

- Bridge (default): Containers on the same host communicate through an internal virtual network. Each container gets its private IP address within the bridge network, and they can reach each other via container names.

- Example: `docker network create my-bridge-network`
- Ideal for running multiple containers on a single host that need to communicate securely without exposing services externally.

- Host: Containers share the host's networking stack and directly use the host’s IP address and ports.

- Example: `docker run --network host nginx`
- Useful when you need high performance and don’t require network isolation, such as running monitoring agents or low-latency applications.

- Overlay: Enables container communication on different hosts by creating a distributed network.

- Example: `docker network create --driver overlay my-overlay-network`
- Designed for orchestrated deployments like Docker Swarm, where services span multiple nodes.

- Macvlan: Assigns a unique MAC address to each container, making it appear as a physical device on the network.

- Example: `docker network create -d macvlan --subnet=192.168.1.0/24 my-macvlan`
- Used when containers need direct network access, such as when integrating legacy systems or interacting with physical networks.

### Running containers on custom networks

Let’s walk through how to set up and use a custom bridge network for container communication.

#### Step 1: Create a custom network

Before running containers, we first need to create a dedicated network:

`docker network create my-custom-network`

[](https://app.datacamp.com/workspace)

This command creates an isolated network that containers can join for inter-container communication.

#### Step 2: Run containers on the network

Now, let’s start two containers and connect them to our newly created network:

`docker run -d --network my-custom-network --name app1 my-app docker run -d --network my-custom-network --name app2 my-app`

[](https://app.datacamp.com/workspace)

- The `--network my-custom-network` flag attaches the container to the specified network.
- The `--name` flag assigns a unique container name, making it easier to reference.

Both `app11 and` app2 `can now communicate using their container names. You can test the connectivity using the` ping` command inside one of the containers:

`docker exec -it app1 ping app2`

[](https://app.datacamp.com/workspace)

If everything is set up correctly, you’ll see a response confirming that the containers can communicate.

### Inspecting Docker networks

To verify network configurations and connected containers, use:

`docker network inspect my-custom-network`

[](https://app.datacamp.com/workspace)

This command provides details about the network, including IP ranges, connected containers, and configurations.

### Exposing and publishing ports

When running containers that need to be accessible externally, you can expose specific ports.

For example, to run an Nginx web server and expose it on port 8080 of your local machine, use:

`docker run -d -p 8080:80 nginx`

[](https://app.datacamp.com/workspace)

This maps port 80 inside the container to port 8080 on the host, making the service accessible via [http://localhost:8080](http://localhost:8080/).

### Best practices for Docker networking

- Use custom networks: Avoid using the default bridge network for production deployments to reduce unintended access between containers.
- Leverage DNS-based discovery: Instead of hardcoding IP addresses, use container names to enable dynamic service discovery.
- Restrict external exposure: Use firewalls or network policies to control service access.
- Monitor traffic: Use tools like `docker network inspect`, Wireshark, or Prometheus to analyze network traffic and detect anomalies.
- Optimize overlay networks: If deploying in a distributed setup, tune overlay networks for reduced latency by leveraging host-local routing options.

## Docker Best Practices and Next Steps

Now that you’ve learned the fundamentals of Docker, it’s time to level up your skills and adopt best practices that will help you build secure, efficient, and maintainable containerized applications.

The following best practices will help you streamline your Docker workflows and avoid common pitfalls.

- Use official base images: Always prefer official and well-maintained base images to ensure security and stability. Official images are optimized, regularly updated, and less likely to contain vulnerabilities.
- Keep images small: Reduce image size by choosing minimal base images (e.g., `python:3.9-slim` instead of `python:3.9`). Remove unnecessary dependencies and files to optimize storage and pull times.
- Use multi-stage builds: Optimize Dockerfiles by separating build and runtime dependencies. Multi-stage builds ensure that only the necessary artifacts are included in the final image, reducing size and attack surface.
- Tag images properly: Always use versioned tags (e.g., `my-app:v1.0.0`) instead of `latest` to avoid unexpected updates when pulling images.
- Scan images for vulnerabilities: Use security scanning tools like `docker scan`, `Trivy`, or `Clair` to identify and remediate security vulnerabilities in your images before deployment.
- Manage environment variables securely: Avoid storing sensitive credentials inside images. Use Docker secrets, environment variables, or external secret management tools like AWS Secrets Manager or HashiCorp Vault.
- Use .dockerignore files: Exclude unnecessary files (e.g., `.git, node_modules`, `venv`) to reduce build context size and prevent accidental inclusion of sensitive files in images.
- Enable logging and monitoring: Utilize tools like Prometheus, Grafana, and Fluentd for container logs and monitoring. Inspect logs using `docker logs` and enable structured logging for better observability.

Once you've mastered the basics of Docker, there are plenty of advanced topics to explore. Here are a few areas worth exploring next:

- Docker Swarm & Kubernetes: Explore Docker Swarm (built-in clustering) and [Kubernetes](https://www.datacamp.com/tracks/containerization-and-virtualization) (enterprise-grade orchestration with auto-scaling and service discovery) for production-grade orchestration.
- Container security best practices: To secure containerized applications, follow the CIS Docker Benchmark guidelines and implement Role-Based Access Control (RBAC).
- CI/CD pipelines with Docker: Automate image builds, security scans, and deployments using GitHub Actions, GitLab CI, or Jenkins.
- Cloud-native development: Leverage Docker with cloud platforms like AWS ECS, Azure Container Instances, and Google Cloud Run for scalable and managed deployments.
- Data persistence strategies: For optimal storage management, understand the differences between Docker volumes, bind mounts, and tmpfs.
up:: [[Docker MOC]]
