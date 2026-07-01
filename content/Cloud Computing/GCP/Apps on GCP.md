

## What is an App?

- Short for **application**.
    
- Self-contained software program designed to perform specific tasks.
    
- Range: simple (calculator) → complex (sales management systems).
    

## Streaming App Example

- **Spotify** → subscription-based streaming service.
    
- Provides music, podcasts, and video streaming.
    
- Demonstrates how apps encapsulate comprehensive service offerings.
    

## Spotify’s Needs

- Store/manage large volumes of user data.
    
- Deliver robust, highly available service.
    
- Compete in fast-moving digital space → continuous analysis and innovation.
    
- Uses GCP services:
    
    - **Cloud Storage** → user data.
        
    - **Google Kubernetes Engine (GKE)** → containerized workloads & microservices.
        
    - **BigQuery** → analytics on vast datasets.
        

## Cloud-Native Apps

- Built specifically for cloud environments.
    
- Benefits:
    
    - Rapid deployment and updates.
        
    - Scalability → handle increased user load.
        
    - Resilience → recover quickly from failures.
        
    - High availability and reliability.
        

## Migrating Apps to the Cloud

- Requires logistics and planning.
    
- **Change patterns** → structured approaches to manage risks.
    
- Factors to assess:
    
    - Complexity of legacy systems.
        
    - Availability of technical resources.
        
    - Business goals and timelines.
        

## Strangler Fig Pattern

- Gradual replacement of monolithic system parts with microservices.
    
- Steps:
    
    - Modernize one function → host as microservice in cloud.
        
    - Remove corresponding functionality from legacy app.
        
    - Repeat until entire app is re-architected.
        
- Suitable for quick scalability, frequent updates, consistent performance.
    
- Requires technical expertise and risk management.
    

## Banking App Modernization

- Example: bank modernizing online banking app.
    
- **Digital wallet** → standalone container deployed on GKE.
    
- Transactions captured with **Cloud Spanner** → scalability + concurrent handling.
    
- **Financial dashboard** → built with BigQuery + Looker.