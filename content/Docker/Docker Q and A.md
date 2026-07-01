### 1. What is Docker?

Docker is a **containerization platform** that packages an application and its dependencies into a **container**, ensuring it runs consistently across different environments (dev, test, prod).

---

### 2. What problem does Docker solve?

- “Works on my machine” issues
    
- Dependency conflicts
    
- Slow environment setup
    
- Inconsistent deployments
    

---

### 3. What is a Docker container?

A **lightweight, isolated runtime environment** that shares the host OS kernel but has its own filesystem, processes, and network.

---

### 4. Difference between Docker containers and Virtual Machines?



|Containers|Virtual Machines|
|---|---|
|Share host OS kernel|Each has its own OS|
|Lightweight|Heavy|
|Fast startup|Slow startup|
|Less resource usage|High resource usage|
### 5. What is a Docker image?

A **read-only blueprint** used to create containers.  
It contains:

- Application code
    
- Dependencies
    
- Runtime
    
- OS libraries
    

---

### 6. What is Docker Hub?

A **public registry** for storing and sharing Docker images (like GitHub for images).

---

## 🔹 Intermediate Docker Interview Questions

### 7. What is a Dockerfile?

A **text file with instructions** to build a Docker image.

Example:

`FROM python:3.11 WORKDIR /app COPY . . RUN pip install -r requirements.txt CMD ["python", "app.py"]`

---

### 8. Explain `FROM`, `RUN`, `COPY`, `CMD`

- `FROM` → base image
    
- `RUN` → executes commands during build
    
- `COPY` → copies files into image
    
- `CMD` → default command when container starts
    

---

### 9. Difference between `CMD` and `ENTRYPOINT`?

|CMD|ENTRYPOINT|
|---|---|
|Can be overridden easily|Harder to override|
|Default command|Main command|

👉 Often used together for flexibility.

---

### 10. What is Docker Compose?

A tool to **run multi-container applications** using a `docker-compose.yml` file.

Used for:

- Microservices
    
- Airflow + Postgres
    
- App + DB setups
    

### 11. What is a Docker volume?

A **persistent storage mechanism** that keeps data even if the container is removed.

---

### 12. Difference between volume and bind mount?

|Volume|Bind Mount|
|---|---|
|Managed by Docker|Managed by host|
|Safer|Less portable|
|Recommended|Dev only|

---

### 13. How does Docker networking work?

Docker provides:

- Bridge network (default)
    
- Host network
    
- Overlay network (Swarm/K8s)
    

Containers communicate using **service names** in Compose.

---

## 🔹 Advanced Docker Interview Questions

### 14. What is a multi-stage Docker build?

Used to **reduce image size** by separating build and runtime stages.

`FROM node:18 AS build RUN npm install  FROM node:18-alpine COPY --from=build /app /app`

---

### 15. How do you reduce Docker image size?

- Use `alpine` images
    
- Multi-stage builds
    
- Remove cache files
    
- Use `.dockerignore`
    

---

### 16. How does Docker handle security?

- Namespace isolation
    
- Control groups (cgroups)
    
- Non-root containers
    
- Image scanning
    

---

### 17. What happens when a container crashes?

- It stops
    
- Can be restarted automatically using `restart` policy
    

`restart: always`

---

### 18. Difference between `docker run` and `docker start`?

- `docker run` → creates + starts container
    
- `docker start` → starts existing container
    

---

### 19. What is Docker Swarm?

Docker’s **native orchestration tool** for managing clusters (lighter than Kubernetes).

---

### 20. Docker vs Kubernetes?

|Docker|Kubernetes|
|---|---|
|Container platform|Container orchestration|
|Single host focus|Multi-node clusters|
|Simple|Complex but powerful|

---

## 🔹 Scenario-Based Interview Questions (🔥 VERY IMPORTANT)

### 21. How would you dockerize a Python app?

1. Create Dockerfile
    
2. Choose base image
    
3. Install dependencies
    
4. Copy code
    
5. Define CMD
    
6. Build and run
    

---

### 22. How would you run Airflow with Postgres?

Use **Docker Compose** with:

- Airflow Webserver
    
- Scheduler
    
- Worker
    
- Postgres DB
    
- Redis (optional)
    

👉 This ties directly to **data engineering interviews**.

---

### 23. How do containers communicate in Docker Compose?

Using **service names** as hostnames.

---

### 24. How do you debug a Docker container?

- `docker logs`
    
- `docker exec -it container bash`
    
- `docker inspect`
    

---

### 25. Common Docker mistakes?

- Running as root
    
- Hardcoding secrets
    
- Large images
    
- Not using volumes
    

---

## 🔹 Quick Fire Commands (Expect These!)

`docker ps docker images docker build -t myapp . docker run -d -p 8000:8000 myapp docker exec -it container bash docker logs container docker-compose up -d`

---

## 🔹 Interview Tip (Important)

If asked **“Do you have Docker experience?”**, say:

> “Yes, I’ve used Docker to containerize Python applications and orchestrate multi-service setups using Docker Compose, including databases and workflow tools like Airflow.”

That’s **entry-level → mid-level strong**.

---


up:: [[Docker MOC]]
