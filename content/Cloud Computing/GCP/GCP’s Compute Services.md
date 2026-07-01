

## Engines and Functions

- **Compute Engine** → customizable virtual machines (server-based, hardware-specific).
    
- **App Engine** → serverless platform for efficient app development and scaling.
    
- **Cloud Functions** → event-driven, lightweight, task-specific applications.
    

## Serverless Spectrum

- **Cloud Functions → App Engine → Compute Engine**
    
- Progression: less resource management → more control.
    
- Trade-off: convenience vs. customization of hardware/software environment.
    

## Microservices in Containers

- Containers package code, dependencies, and data.
    
- Enable breaking large applications into smaller, manageable microservices.
    
- Each containerized service performs a specific function.
    

## Photo-Sharing App Example

- Microservices for uploads, downloads, recommendations.
    
- Surge in uploads → scale up upload containers.
    
- Uploads trigger recommendation updates.
    
- Highlights need for container orchestration.
    

## Kubernetes & GKE

- **Kubernetes** → open-source container orchestration (invented by Google).
    
- **Google Kubernetes Engine (GKE)** → fully managed Kubernetes solution.
    
- Automates scaling, updates, and integrates with GCP services (Cloud Storage, BigQuery).
    
- Example: surge in uploads → GKE scales upload containers, passes messages to recommendation containers.
    

## Hybrid Architectures

- Some data may remain on-premises (e.g., sensitive analytics).
    
- Need for communication between on-prem servers and cloud microservices.
    

## Anthos

- Unified management across GCP, other clouds, and on-premises.
    
- Consistent deployment, scaling, and compliance.
    
- Requires container-based architecture.
    
- Facilitates modernization of legacy applications by shifting them into containers.