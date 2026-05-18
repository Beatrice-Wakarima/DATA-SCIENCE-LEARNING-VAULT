## What is Cloud Run? 

Cloud Run is a serverless container execution platform that allows you to deploy applications without worrying about infrastructure management. 

With traditional server-based deployments, you usually have to provision and maintain virtual machines. Cloud Run works slightly differently, and abstracts all of that away to offer a fully managed environment. 

It’s built on Knative (an open-source [Kubernetes](https://www.datacamp.com/blog/what-is-kubernetes)-based platform that enables serverless workload), meaning your application scales automatically based on demand. When traffic increases, Cloud Run spins up more instances to handle it. When traffic drops, it scales down. It can even go all the way to zero, so you won’t pay anything when your app isn’t actively running.

Cloud run is cost-efficient, but it is also super flexible. You can deploy applications written in any language and use any framework or binary, as long as it runs in a container. You can work with common technologies like Node.js, Python, Go, Java, or more obscure ones. Practically, that means that Cloud Run can power backend services, APIs, AI workloads, web apps, and even scheduled batch jobs. 

That was for the sneak peek. Let’s get a bit deeper into the key features of Cloud Run.

## Key Features of Cloud Run

We have just mentioned a couple, but here is a full rundown of Cloud Run’s main features.

### Language and framework agnostic

One of Cloud Run’s biggest advantages is that it doesn’t lock you into a specific language or framework. As long as your application runs in a container, you can deploy it. If you are a team working with a diverse tech stack, you can use Cloud Run across all your services. One tool to rule them all!

### Automatic scaling

Cloud Run scales horizontally and dynamically based on traffic. If your application receives more requests, Cloud Run automatically spins up more instances. When demand drops, it scales down, all the way to zero if needed.

### Built-in security and compliance

Cloud Run comes with automatic HTTPS for all deployed services, google-managed service identity for secure authentication, VPC connectivity for private networking and built-in compliance certifications like SOC 2, ISO 27001, and HIPAA (for healthcare applications). Basically, you’re in good hands.

### Integration with Google Cloud services

Since Cloud Run is part of the Google Cloud ecosystem, it plays well with other GCP services. You can easily connect it to Cloud SQL for databases, stream data with Pub/Sub, store files in Cloud Storage or use it with BigQuery, Firebase, and AI/ML services.

### On-demand GPU support

For AI workloads, Cloud Run now offers on-demand GPU support. This is a great improvement for machine learning inference, video processing, and scientific computing, because it allows you to run any GPU-accelerated workloads without managing the hardware behind it.

### Cloud Run Functions: A Function-as-a-Service (FaaS) model

If you don’t want to manage full containers, Cloud Run Functions provides a simplified, event-driven way to run small, single-purpose functions. It’s similar to AWS Lambda or Google Cloud Functions but runs on Cloud Run’s infrastructure.

## How Cloud Run Works: Step-by-Step

In this section, I’ll walk you through how to deploy a simple application to Cloud Run. I will guide you through the process of containerizing your app, deploying it to Cloud Run, and scaling it automatically based on demand.

We’ll use Docker to containerize our application, but you don’t necessarily have to. More on that at the end.

### Step 1: Set up your environment

Before deploying anything, you need to have the following tools installed:

1. Google Cloud SDK: This is a command-line interface (CLI) that allows you to interact with Google Cloud services, including Cloud Run. You can install it from [here](https://cloud.google.com/sdk/docs/install).
2. Docker: If your app isn't already containerized, you’ll need Docker to package your app. Install Docker from [here](https://docs.docker.com/engine/install/).
3. Google Cloud Project: Ensure you have a Google Cloud project set up. You can create one from the [Google Cloud Console](https://console.cloud.google.com/).

### Step 2: Write your application code

Now, let’s write a simple “Hello World” Node.js application.

Create a directory for your app:

`mkdir hello-world-app cd hello-world-app`

[](https://app.datacamp.com/workspace)

Create an index.js file inside the directory with the following content:

`const http = require('http');  const requestListener = (req, res) => {     res.writeHead(200);     res.end('Hello, Cloud Run!'); };  const server = http.createServer(requestListener); server.listen(8080, () => {     console.log('Server is running on port 8080'); });`

[](https://app.datacamp.com/workspace)

Create a package.json to define your app’s dependencies:

`{     "name": "hello-world-app",     "version": "1.0.0",     "main": "index.js",     "dependencies": {} }`

[](https://app.datacamp.com/workspace)

Now that the application is ready, we’ll proceed to containerizing it.

### Step 3: Containerize the application

#### Create a Dockerfile to define the container image

In your project directory, create a file named “Dockerfile” with the following content:

`# Use the official Node.js image as a base FROM node:16-alpine  # Set the working directory inside the container WORKDIR /usr/src/app  # Copy package.json and install dependencies (if any) COPY package*.json ./  # Copy the rest of the application code COPY . .  # Expose port 8080 for Cloud Run EXPOSE 8080  # Start the app CMD ["node", "index.js"]`

[](https://app.datacamp.com/workspace)

#### Build the Docker image

Run the following command to build your Docker image:

`docker build -t gcr.io/your-project-id/hello-world-app .`

[](https://app.datacamp.com/workspace)

Note: Replace your-project-id with your Google Cloud project ID.

#### Test the image locally

You can test your Docker container locally by running:

`docker run -p 8080:8080 gcr.io/your-project-id/hello-world-app`

[](https://app.datacamp.com/workspace)

Visit http://localhost:8080 in your browser to verify the app is running.

### Step 4: Push the image to Google Artifact Registry

#### Enable Artifact Registry for your project

If you haven’t already enabled Artifact Registry, run the following command

`gcloud services enable artifactregistry.googleapis.com`

[](https://app.datacamp.com/workspace)

Note: You will need to enable billing to complete this step!

#### Create a repository in Artifact Registry

Create a new Docker repository in Artifact Registry:

`gcloud artifacts repositories create hello-world-repo \ --repository-format=docker \ --location=us-central1`

[](https://app.datacamp.com/workspace)

#### Authenticate Docker to Artifact Registry

Configure Docker to authenticate with Artifact Registry:

`gcloud auth configure-docker us-central1-docker.pkg.dev`

[](https://app.datacamp.com/workspace)

#### Tag the Docker image for Artifact Registry

Tag your Docker image with the Artifact Registry repository URL:

`docker tag gcr.io/your-project-id/hello-world-app us-central1-docker.pkg.dev/your-project-id/hello-world-repo/hello-world-app`

[](https://app.datacamp.com/workspace)

#### Push the image to Artifact Registry

Push the tagged Docker image to your Artifact Registry repository:

`docker push us-central1-docker.pkg.dev/your-project-id/hello-world-repo/hello-world-app`

[](https://app.datacamp.com/workspace)

### Step 5: Deploy to Cloud Run

Once your image is pushed to Artifact Registry, you can deploy it to Cloud Run directly from Artifact Registry.

Deploy your image to Cloud Run using the following command:

`gcloud run deploy hello-world-app \ --image us-central1-docker.pkg.dev/your-project-id/hello-world-repo/hello-world-app \ --platform managed \ --region us-central1 \ --allow-unauthenticated`

[](https://app.datacamp.com/workspace)

- hello-world-app: This is the name of your Cloud Run service.
- us-central1-docker.pkg.dev/your-project-id/hello-world-repo/hello-world-app: The URL for your image stored in Artifact Registry.
- --platform managed: Ensures the deployment uses Cloud Run’s fully managed platform (not a GKE cluster).
- --region us-central1: Specify the region where Cloud Run should deploy the service.
- --allow-unauthenticated: This allows public access to the service. If you need restricted access, you can adjust this flag accordingly.

After running this command, Cloud Run will deploy your containerized application and provide you with a URL to access it.

And we’re all done! Have a look in the GCP console, you should see your new instance.

### Step 6: Clean up

To avoid any ongoing charges, make sure to delete your service once you're done testing.

#### 1. Delete the Cloud Run service

Run the following command to delete your deployed Cloud Run service:

`gcloud run services delete hello-world-app --region us-central1`

[](https://app.datacamp.com/workspace)

This removes the Cloud Run instance but does not delete the container image.

#### 2. Delete the Artifact Registry image

To remove the image from Artifact Registry, first list the images:

`gcloud artifacts docker images list us-central1-docker.pkg.dev/your-project-id/hello-world-repo`

[](https://app.datacamp.com/workspace)

Then, delete the image with:

`gcloud artifacts docker images delete us-central1-docker.pkg.dev/your-project-id/hello-world-repo/hello-world-app --delete-tags`

[](https://app.datacamp.com/workspace)

Now your Artifact Registry is cleaned up as well.

#### 3. Delete the Artifact Registry repository (if no longer needed)

If you want to completely remove the Artifact Registry repository, run:

`gcloud artifacts repositories delete hello-world-repo --location=us-central1`

[](https://app.datacamp.com/workspace)

This step is only necessary if you're done with the repository entirely, otherwise, you can reuse it for future deployments.

#### 4. (Optional) Delete the Google Cloud project

If this was a test project and you no longer need it, you can delete the whole project to remove all associated resources:

`gcloud projects delete your-project-id`

[](https://app.datacamp.com/workspace)

### Source deployments

Remember when I said you don’t always have to containerize your app manually?

Cloud Run now supports source deployments, which means it can build the container for you from your source code, using Cloud Build.

You can use the command:

`gcloud run deploy hello-world-app \ --source . \ --region us-central1 \ --allow-unauthenticated`

[](https://app.datacamp.com/workspace)

Cloud Build automatically detects your application’s language (Node.js, Python, Go, Java, etc.), builds a container image for you and stores it in Artifact Registry. Cloud Run then deploys the built image just as if you had manually created a container. I definitely would recommend using this for simple applications with supported languages (Node.js, Python, Go, Java, etc.), but not if you need full control over the container (e.g., custom dependencies, OS-level tweaks, multi-step builds).

## Tips to Use Cloud Run efficiently

Okay, so deploying an app to Cloud Run is pretty easy, but getting it to run efficiently requires a little bit of fine-tuning. I went through a trial-and-error phase when I first starting using it, and this is what I’ve learned:

### 1. Cold starts are real

Especially if you’re working with a large container image. The smaller your image, the faster your service spins up. Using a minimal base image like distroless can make a big difference. If you’re building Python apps, try using slim versions of official images. Or if you’re not bothered about costs too much, set your minimum instance number to 1.

### 2. The best variable to play with is the request concurrency amount

Cloud Run lets each instance handle multiple requests simultaneously, but the default (80 requests per container) is often not the optimal amount. For CPU-intensive tasks, I’ve found that lowering concurrency to 1 or 2 makes things a lot smoother. On the flip side, APIs can usually handle a higher number. The higher the number, the more you can reduce the number of instances you need, and therefore the least you will pay, so it’s definitely worth experimenting with different values to find the sweet spot for your app.

### 3. Set your instance limits!

Super helpful when someone (me) decides to do some load testing and starts a silly number of requests. I learnt that lesson so you don’t have to. Please set your max instance count.

### 4. Make sure you let the right people access your instance

By default, Cloud Run services can be accessed by anyone with the URL, which is great for quick demos but not so great for production. If your app isn’t meant to be public, lock it down with IAM permissions. 

### 5. Cloud Logging and Cloud Trace will become your best friends

If, like me, you tend to debug issues by SSH-ing into virtual machines, you’ll be disappointed. Cloud Run logs are streamed directly to Google Cloud’s dashboard, so you can see everything in there. Make sure you add structured logging to your application, it will make troubleshooting way easier.

## Cloud Run Use Cases

We talked about some use cases of Cloud Run, like running web apps, APIs or cron jobs, but there are obviously a lot more.

### Video and image analysis

You can deploy an image recognition model to process uploaded images in real-time for a social media platform, or run video transcoding tasks when a video is uploaded. Cloud Run can handle spikes in demand (like viral content) with its automated scaling, while ensuring cost-efficiency when demand is low.

![Video and image analysis](https://media.datacamp.com/cms/ad_4nxcnrhfddjllreumdimug6bqqm3i06bthx6bnbs2iacuv1vd4hyk42ogx1syfzitya85mt7exqycf4iwnovdsxusygzjy8ffdmnpgzw43_lt6qqug7ohd2mjyl_b47d3tlulczed.png)

_Source:_ [_Google Cloud_](https://cloud.google.com/functions#integration-with-third-party-services-and-apis)

### Real-time stream processing

Imagine you’re building a system that monitors user behavior on an online marketplace. By [processing event streams](https://www.datacamp.com/blog/batch-vs-stream-processing) from Pub/Sub or BigQuery, you can instantly trigger actions based on user activity, like sending push notifications or analyzing trends in real time. Cloud Run automatically scales up to handle incoming events during peak periods and scales down when the volume of streams decreases.

![Real-time stream processing](https://media.datacamp.com/cms/ad_4nxf84gaj-kg2urxmfotxmcy5vczv92szlbmpp5yebnzoqvdby1nwt59dv7gap_uratjqncc4e78xhpylrtn20mryhq9k2znlcet_lxuichmwjhehl0hlwuqtxlgzftoh1k0uj7ejmw.png)

_Source:_ [_Google Cloud_](https://cloud.google.com/functions#integration-with-third-party-services-and-apis)

### Real-time file processing

A use case could be real-time log file analysis for a large enterprise. Whenever a log file is uploaded to Cloud Storage, Cloud Run can trigger a container to parse the file, run analysis, and store the results, all while scaling dynamically based on the file size and complexity of the processing task.

![Real-time file processing](https://media.datacamp.com/cms/ad_4nxe4gb7y4asdalfkvn9wqhniu2nnpenwasg0s4wgbsgudmpt_kdkyydbnbbuxcourl4i06afgo4t3zqbb2qqpja5pf814fphvhwxoa24bprkw8ayi5mtwztjhcjupby0mur8e512.png)

_Source:_ [_Google Cloud_](https://cloud.google.com/functions#integration-with-third-party-services-and-apis)

### Serverless IoT backends

Cloud Run is ideal for handling backend services for IoT applications. For example, in an IoT solution that tracks environmental data from thousands of sensors, Cloud Run can process the incoming data from each device in real-time.

![Serverless IoT backends](https://media.datacamp.com/cms/ad_4nxfjy0zy5oftxfd1ggcsxvzwk8mnsb3vh1ilnt-8lrhsewwynluqxsdh-nssrrhakrw-mqcvdn8zhy7ayxnwx3nva9bq99hhzfqnoqcglrh9erec6m--crs8ztl8-w09hwkxzgbdxw.png)

_Source:_ [_Google Cloud_](https://cloud.google.com/functions#integration-with-third-party-services-and-apis)

## Google Cloud Run Pricing 

Cloud Run follows a pay-as-you-go model, meaning you only pay for the compute resources used while your application is actively running. When your app isn’t handling requests, it can scale down to zero, which means you don’t pay unnecessary costs.

### Pricing Breakdown

As of March 2025, Cloud Run charges based on two main factors:

|Resource|Cost|Free Tier|
|---|---|---|
|CPU|$0.000018 per vCPU-second|240,000 vCPU-seconds/month|
|Memory|$0.000002 per GiB-second|450,000 GiB-seconds/month|

This pricing is for instance-based billing, but it works differently for request-based billing. The price above and free tier are also slightly different depending on the region you’re in, so check the [official Google Cloud page](https://cloud.google.com/run/pricing/?_gl=1*16oykqt*_up*MQ..&gclid=Cj0KCQjwm7q-BhDRARIsACD6-fWnvcIjJj5lAZscPU_hO1YHPrQPkG7xy_BDgZ51cUBo3IMu1njemFUaAuwEEALw_wcB&gclsrc=aw.ds) for the exact numbers. They have a price calculator to help you figure out the costs, and they also offer discounts for committed use.

Little tip: Traffic with other Google Cloud services in the same region is free, so try using Cloud Storage, Cloud SQL, or Pub/Sub instead of external services for data exchange.

## Cloud Run vs. Cloud Run Functions 

Google offers two serverless compute options: Cloud Run and [Cloud Run Functions](https://cloud.google.com/functions?hl=en) (previously Cloud Functions). They both allow you to run code without managing infrastructure, but they’re slightly different.

|Feature|Cloud Run|Cloud Functions|
|---|---|---|
|**Execution Model**|Runs full containerized applications|Runs individual functions (FaaS model)|
|**Runtime Control**|Any language, any framework, custom binaries|Predefined runtimes (Node.js, Python, Go, etc.)|
|**State**|Stateless, but can maintain connections within a request|Stateless, designed for event-driven workloads|
|**Scaling**|Scales per container instance|Scales per function invocation|
|**Triggering**|HTTP requests, Pub/Sub, event-driven|Event-driven (Pub/Sub, Cloud Storage, HTTP, etc.)|
|**Cold Starts**|Minimal with pre-warmed instances|Can have noticeable delays in scaling|
|**Best For**|APIs, microservices, backend services, AI workloads|Lightweight, event-driven functions, automation|

When to Use Cloud Run

- ✅ You need full control over the runtime and dependencies.
- ✅ You’re running a web service, API, or microservice that handles persistent requests.
- ✅ You want to deploy an existing containerized application with minimal modification.
- ✅ You need background processing or long-running tasks (like AI inference, batch jobs).

When to Use Cloud Run Functions

- ✅ You want simple, event-driven functions that trigger on events like Pub/Sub messages or Cloud Storage uploads.
- ✅ You’re handling short-lived operations like sending notifications, processing small jobs, or transforming data.
- ✅ You don’t want to manage containers and prefer prebuilt runtimes for JavaScript, Python, Go, etc.

You don’t necessarily have to choose though, you can use both together! For example, your Cloud Run backend could trigger Cloud Run Functions for specific tasks like sending emails or processing images asynchronously.

## Comparisons to Other Google Cloud Services

We have compared Cloud Run and Cloud Run Functions quite thoroughly, but there might be a couple of other Google Cloud services worth mentioning here: GKE and App Engine.

|Feature|Cloud Run|Google Kubernetes Engine (GKE)|App Engine|
|---|---|---|---|
|**Management Type**|Fully managed serverless|Self-managed Kubernetes clusters|Fully managed platform-as-a-service|
|**Scaling**|Automatic scaling, down to zero|Manual scaling or auto-scaling via Kubernetes|Automatic scaling (but not down to zero)|
|**Deployment**|Deploy containers (any language)|Deploy containers via Kubernetes|Deploy code (specific runtimes supported)|
|**Use Cases**|APIs, microservices, web apps, batch jobs, AI|Complex apps, large-scale microservices, ML workloads|Web apps, mobile backends, APIs|
|**Supported Languages**|Any (container-based)|Any (container-based)|Specific runtimes supported|

There is obviously more nuance to this, but in short: If you need a fully managed, containerized solution with automatic scaling and flexibility, go for Cloud Run. If you're building a web app with minimal configuration, go for App Engine. And if you want full control over your Kubernetes clusters for large-scale, complex applications, choose GKE.