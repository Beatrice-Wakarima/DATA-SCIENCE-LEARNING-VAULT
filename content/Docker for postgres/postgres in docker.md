### Benefits of running PostgreSQL in Docker

Docker gives you an elegant way to run PostgreSQL databases. It offers a couple of no-brainer benefits when compared to traditional installation methods:

- Simplified installation and setup: With Docker, you can spin up a PostgreSQL instance with just one command. No more dealing with package managers, system dependencies, or complicated installation scripts. The database comes pre-configured with sensible defaults and is ready to use immediately.
- Consistent environments across teams: Everyone on your team gets exactly the same PostgreSQL setup, regardless of their operating system. This eliminates the "it works on my machine" problem that's common in development teams.
- Isolation from other system components: Docker containers run in isolation, which means your PostgreSQL instance won't interfere with other software on your machine. You can run multiple versions of PostgreSQL at the same time without conflicts, and removing PostgreSQL is as simple as stopping and removing the container.
- Version control for your database environment: Docker allows you to specify exact PostgreSQL versions in your configuration files. This means you can make sure development environments match production exactly, and you can test upgrades in isolation before applying them to production systems.
- Resource efficiency: Docker containers are lightweight compared to virtual machines. They use fewer system resources and provide similar isolation benefits. This means you can run PostgreSQL alongside other containers without significantly impacting system performance.

### When to use PostgreSQL in Docker

For the sake of convenience, I'll just name a few:

- Local development environments: For developers working on applications that use PostgreSQL, Docker provides a quick way to get started without altering their local system. You can easily match the exact database version and configuration used in production, which ensures the code that works locally will work when deployed.
- Microservices architecture: If you're building applications using microservices, Docker lets each service have its own database instance if needed. This provides better isolation between services and allows teams to manage their database dependencies independently.
- CI/CD pipelines and automated testing: Docker makes it simple to create fresh database instances for running tests. Each test run can start with a clean database state, which improves test reliability. 
- Development of database migration scripts: Docker provides a safe environment for testing database migrations. You can verify your migration scripts against a disposable database that matches your production environment before you apply them to real systems.
- Kubernetes deployments: If you're using Kubernetes for orchestration, running PostgreSQL in Docker is a natural fit. Your local development environment can closely match your production Kubernetes setup, making the development-to-production workflow seamless.

In short, Dockerized PostgreSQL is useful for development and testing, but it's worth noting that managing production database deployments requires additional considerations around data persistence, backups, and high availability.

I'll touch on some of these considerations in later sections of this article.

## Setting Up PostgreSQL in Docker

The only thing you'll need to run the Postgres database in Docker is the Docker engine itself.

In this section, I'll walk you through the process of covering the prerequisites and running a fully functional PostgreSQL database in a Docker container.

### Prerequisites

Before getting started with PostgreSQL in Docker, you'll need Docker installed on your system.

Installation varies by operating system. Windows and macOS users can simply install Docker Desktop, which is an easy-to-use graphical interface for managing containers. Download it from the [official Docker website](https://www.docker.com/products/docker-desktop/).

Linux users can install Docker Engine directly using their distribution's package manager. For example, on Ubuntu:

`sudo apt update sudo apt install docker.io sudo systemctl enable --now docker`

[](https://app.datacamp.com/workspace)

In addition to having Docker installed, it's recommended that you're familiar with basic terminal commands and basic Docker concepts, such as images, containers, and volumes. These practical guides from DataCamp have you covered:

- [Docker for Beginners: A Practical Guide to Containers](https://app.datacamp.com/learn/tutorials/docker-tutorial)
- [Install Docker on Ubuntu: From Setup to First Container](https://app.datacamp.com/learn/tutorials/install-docker-on-ubuntu)

### Pulling the PostgreSQL Docker image

Before running PostgreSQL, you need to download the official PostgreSQL Docker image from [Docker Hub](https://hub.docker.com/_/postgres). This image serves as a template for creating containers.

To pull the latest PostgreSQL image, open your terminal or command prompt and run:

`docker pull postgres`

[](https://app.datacamp.com/workspace)

This command downloads the latest stable version of PostgreSQL. If you need a specific version, you can specify it with a tag:

`docker pull postgres:17`

[](https://app.datacamp.com/workspace)

![Image 1 - Pulling the latest stable version of PostgreSQL database image](https://media.datacamp.com/cms/ad_4nxc9xi8rkjpaem3mazzj2nffyxzvc5xtizikxa0h5-r_mfbt4dxome79ekmbzjdfv3dawat0jdrqi_hfnzuwwhygqe8wer7k-_w2pwqddxvyutssboxteqazntyo35wint3wmsqpya.png)

_Image 1 - Pulling the latest stable version of PostgreSQL database image_

Some commonly used PostgreSQL image tags include:

- `postgres:latest` - The most recent stable PostgreSQL version
- `postgres:17` - PostgreSQL version 14.x (the most recent patch of version 17)
- `postgres:17.4` - A specific version (17.4 in this case).
- `postgres:bookworm` - PostgreSQL built on Debian Bookworm Linux distribution.

You can view all available tags on the [official PostgreSQL Docker Hub page](https://hub.docker.com/_/postgres/tags).

### Running PostgreSQL in a Docker container

Once you have the PostgreSQL image, you can create and start a container with a single command:

`docker run --name postgres-db -e POSTGRES_PASSWORD=mypassword postgres`

[](https://app.datacamp.com/workspace)

![Image 2 - Starting a PostgreSQL container](https://media.datacamp.com/cms/ad_4nxdzntlkvd8y5lgkodml8umhj6fuqmzj4zngxghhwau6dtb8mw9yjslshozlkzagncj-yf2uw80xlxvw0sw1rggxf2o0t-r8eiweeossdsmrcyn0n3s6zqlcq13jhndvyvtbckkiuq.png)

_Image 2 - Starting a PostgreSQL container_

This command creates a new container named `postgres-db` and sets an environment variable for the PostgreSQL password.

However, this basic command has limitations. I recommend using additional options:

`docker run --name postgres-db \   -e POSTGRES_PASSWORD=mypassword \   -e POSTGRES_USER=myuser \   -e POSTGRES_DB=mydatabase \   -p 5432:5432 \   -v postgres-data:/var/lib/postgresql/data \   -d postgres`

[](https://app.datacamp.com/workspace)

![Image 3 - Starting a PostgreSQL container with env variables in detached mode](https://media.datacamp.com/cms/ad_4nxcn02bpyzli6vfnndmoycsrf57s1xkzrbulwauuwle4d0yltbjqypmynabyk-0t9zmiyohotretew9wpvebg4me4iq9axsf1iusafh5abm4cbd3t4l2rgc-sueaqni9oc9t2vl6ka.png)

_Image 3 - Starting a PostgreSQL container with env variables in detached mode_

Let me break down these additional options:

- Environment variables:
    - `POSTGRES_PASSWORD`: Sets the password for the PostgreSQL superuser (required).
    - `POSTGRES_USER`: Creates a new superuser with this name (defaults to "postgres" if not specified).
    - `POSTGRES_DB:` Creates a new database with this name (defaults to the username if not specified).
- Port mapping (`-p 5432:5432`) maps the container's PostgreSQL port (5432) to the same port on your host machine, allowing you to connect to PostgreSQL using localhost:5432.
- Volume mounting (`-v postgres-data:/var/lib/postgresql/data`) creates a Docker volume named postgres-data that persists the database files outside the container. This ensures your data isn't lost when the container stops or is removed.
- The `-d` flag makes sure the container runs in detached mode. In plain English, this means the container runs in the background.

You can verify the container is running with:

`docker ps`

[](https://app.datacamp.com/workspace)

![Image 4 - Listing all running containers](https://media.datacamp.com/cms/ad_4nxdlbyifr9usldslijydstygp326uz7tnbwfjiif29e2raq0xcsubsn_g11mmfnnzdefs3e-go_0447lwjmzmn3kmcmu8xuz5hixhoc7xre8sdo7xpsbf3leapwcx8f31ekyd004.png)

_Image 4 - Listing all running containers_

In the next section, I'll show you how to configure your PostgreSQL container further for specific use cases.

## Configuring PostgreSQL in Docker

The basic setup I covered in the previous section will get you started, but for anything more advanced, you'll likely want to customize your PostgreSQL container.

That's what this section is all about.

### Setting up persistent storage with volumes

One of the most important aspects of running a database in Docker is making sure your data persists beyond the lifecycle of the container. By default, all data in a container is lost when the container is removed. For a database, this is rarely what you want.

Docker volumes provide a solution to this problem by storing data outside the container filesystem.

To set it up, start by creating a named volume:

`docker volume create postgres-data`

[](https://app.datacamp.com/workspace)

You can optionally inspect the volume details by running the following command:

`docker volume inspect postgres-data`

[](https://app.datacamp.com/workspace)

![Image 5 - Listing volume details](https://media.datacamp.com/cms/ad_4nxc5zdmkrcn_ti85tiu4pavqeygotadgozc3kqkxgmq0bkn-7yrutgtdpvl-d9u-xozuvheqkqrs9hwnu7uegruzoxvzb5vdbzhsemmthg7qj_btgtqwnexhalkchzdcvnyxmpdeiq.png)

_Image 5 - Listing volume details_

Now, when starting your PostgreSQL container, mount the volume to the PostgreSQL data directory:

`docker run --name postgres-db \   -e POSTGRES_PASSWORD=mysecretpassword \   -v postgres-data:/var/lib/postgresql/data \   -d postgres`

[](https://app.datacamp.com/workspace)

The `-v postgres-data:/var/lib/postgresql/data` parameter connects the named volume to the container's data directory.

To summarize, using volumes for PostgreSQL comes with these advantages:

- Your data persists even if you remove the container.
- You can stop, start, or upgrade your container without losing data.
- You can create backups of your data by backing up the volume.
- Better performance compared to bind mounts (especially on macOS and Windows).

### Exposing ports to connect to PostgreSQL

To connect to your PostgreSQL database from applications running on your host machine, you need to expose the PostgreSQL port (5432) to your local system.

The simplest approach is to map the container's port 5432 to the same port on your host:

`docker run --name postgres-db \   -e POSTGRES_PASSWORD=mysecretpassword \   -p 5432:5432 \   -d postgres`

[](https://app.datacamp.com/workspace)

The `-p 5432:5432` parameter maps the container's port 5432 to port 5432 on your host machine.

If you already have PostgreSQL or another service using port 5432 on your host, you can map to a different port:

`docker run --name postgres-db \   -e POSTGRES_PASSWORD=mysecretpassword \   -p 5433:5432 \   -d postgres`

[](https://app.datacamp.com/workspace)

Now, the container's port 5432 is mapped to port 5433 on your host. When connecting, you'll need to specify port 5433 instead of the default 5432.

By default, the port is exposed on all network interfaces (0.0.0.0). You can optionally restrict it to `localhost` for additional security:

`docker run --name postgres-db \   -e POSTGRES_PASSWORD=mysecretpassword \   -p 127.0.0.1:5432:5432 \   -d postgres`

[](https://app.datacamp.com/workspace)

This allows connections only from your local machine, not from other machines on the network.

### Configuring PostgreSQL settings

You can change many default PostgreSQL settings when spinning up your container. A common approach, but not the only one, is to use environment variables.

Here are a couple of variables you can use to configure the database:

`docker run --name postgres-db \   -e POSTGRES_PASSWORD=mysecretpassword \   -e POSTGRES_USER=myuser \   -e POSTGRES_DB=mydatabase \   -e POSTGRES_INITDB_ARGS="--data-checksums" \   -e POSTGRES_HOST_AUTH_METHOD=scram-sha-256 \   -d postgres`

[](https://app.datacamp.com/workspace)

And here's what each of these does:

- `POSTGRES_PASSWORD`: Sets the superuser password (required).
- `POSTGRES_USER`: Sets the superuser name (defaults to "postgres").
- `POSTGRES_DB`: Sets the default database name (defaults to the user name).
- `POSTGRES_INITDB_ARGS`: Passes arguments to PostgreSQL's `initdb` command.
- `POSTGRES_HOST_AUTH_METHOD`: Sets the authentication method.

In addition to environment variables, you can also go with customizing PostgreSQL configuration to make more advanced changes to the database configuration.

Some frequently customized PostgreSQL settings are:

- `max_connections`: Controls how many connections PostgreSQL accepts (default is 100).
- `shared_buffers`: Sets memory used for caching (default is often too low for production).
- `work_mem`: Memory used for query operations.
- `maintenance_work_mem`: Memory used for maintenance operations.

For a practical implementation, start by creating a file, let's call it `my-postgres-conf`:

`max_connections = 200 shared_buffers = 1GB work_mem = 16MB maintenance_work_mem = 256MB`

[](https://app.datacamp.com/workspace)

Now, mount this file when running the container:

`docker run --name postgres-db \   -e POSTGRES_PASSWORD=mysecretpassword \   -v ./my-postgres.conf:/etc/postgresql/postgresql.conf \   -v postgres-data:/var/lib/postgresql/data \   -d postgres \   -c 'config_file=/etc/postgresql/postgresql.conf'`

[](https://app.datacamp.com/workspace)

Long story short, by configuring persistence, network access, and PostgreSQL settings properly, you can create a Docker-based PostgreSQL environment that runs exactly as you want. The base `postgres:latest` image is just that - the base - there's a lot you can tweak.

In the next section, I'll show you how to connect to the PostgreSQL database running in Docker.

## Connecting to PostgreSQL Running in Docker

Now that you have your PostgreSQL container up and running, the next step is to connect to it. After all, why else would you run a database?

In this section, I'll show you two ways to connect to your containerized PostgreSQL database: using the command-line psql tool and using a graphical interface.

For reference, I'm running my database container with this command:

`docker run --name postgres-db \   -e POSTGRES_PASSWORD=mysecretpassword \   -e POSTGRES_USER=myuser \   -e POSTGRES_DB=mydatabase \   -v postgres-data:/var/lib/postgresql/data \   -p 5432:5432 \   -d postgres`

[](https://app.datacamp.com/workspace)

### Connecting using the psql command line tool

The psql command-line tool is the official PostgreSQL client that lets you interact with the database using SQL commands. 

To connect to the PostgreSQL database running in the container from your host machine, run the following command, but remember to update user and database values:

`docker exec -it postgres-db psql -U myuser -d mydatabase`

[](https://app.datacamp.com/workspace)

![Image 6 - Connecting to Postgres database using psql](https://media.datacamp.com/cms/ad_4nxehhskcvscsuni3jzelgqz3inumwygqqoqskutjseqwnzvhvc4camjhqp2cfsjghot6qsjjifnfjwygj5pbg5jzcqbbgd96tvwtzbks9sih2bwwabha_yznthmkqnc5ad9d3wajrw.png)

_Image 6 - Connecting to Postgres database using psql_

And that's it!

If you're not sure what the command does, here's a simple breakdown:

- `docker exec -it postgres-db`: Run an interactive command inside the container named "postgres-db".
- `psql -U myuser -d mydatabase`: Start psql, connecting as "myuser" to the database "mydatabase".

If you're having trouble connecting, check these common issues:

- Confirm the container is running with `docker ps`.
- Verify port mapping with `docker port postgres-db`.

### Connecting using a GUI tool

Many developers prefer using a graphical tool over a CLI - myself included. [pgAdmin](https://www.pgadmin.org/) is a popular and free choice for PostgreSQL, but the connection process is similar for other tools like [DBeaver](https://dbeaver.io/), [DataGrip](https://www.jetbrains.com/datagrip/), or [TablePlus](https://tableplus.com/).

Installation of pgAdmin is straightforward, so I won't cover it here.

Assuming you have it installed and launched, right-click on "Servers" in the browser panel and select "Register > Server". Now, in the General tab, give your connection a name:

![Image 7 - pgAdmin general tab](https://media.datacamp.com/cms/ad_4nxff4_1re6yk796cclrj4_tzwwgyr9-q1nc5u_k6nbhkvnd6lakyxxukhicopfgkqpawcskv9xlm5fxbvrmhldhvy0jt3abxzve6xpzuywen_0yrdeeyqevwi40-tktk8svhfpg4mw.png)

_Image 7 - pgAdmin general tab_

Then switch to the "Connection" tab and enter these details:

- Host name/address: `localhost`
- Port: `5432` (or whatever port you mapped to)
- Maintenance database: `mydatabase`
- Username: `myuser`
- Password: Your PostgreSQL password

![Image 8 - pgAdmin connection tab](https://media.datacamp.com/cms/ad_4nxfhrahbueqo0jkvkwx_q2ecybse_sdzmctwsvefd_rnkp26ig0zpsevutvcdy8vjikvc2jssmtevt8b9esfw4tbyedd7pasqy1cmrzyiwcsfsx9uzvsgnhp-ziiksdet-ctabbkbg.png)

Image 8 - pgAdmin connection tab

Finally, click "Save" to connect:

![Image 9 - Successful connection](https://media.datacamp.com/cms/ad_4nxfcq2dlwqtinquyedpnkwq51pbmqlxj2x7jsx2-4uxn63c40bn88by7gm6xe0u9pqt-lvy_zki5m2n2tfayeh542biu8i1emygvkhoxshgjx6b9uizqkk8ehlg1cptuiofavy3dea.png)

Image 9 - Successful connection

Once you're connected, you can start working with your database just as you would with a locally installed or cloud-provisioned PostgreSQL instance. The beauty of Docker is that from your application or client's perspective, there's no difference—it's just a PostgreSQL database accessible at the specified address.

_>Need programmatic access to your PostgreSQL database? [Learn how to access it from Python](https://app.datacamp.com/learn/tutorials/tutorial-postgresql-python)._

In the next section, I'll cover how to manage your PostgreSQL container, including stopping, starting, and monitoring it.

## Managing PostgreSQL in Docker

It's one thing to run a PostgreSQL database in a container and connect to it, but management is a whole different animal. Luckily for you, there's a handful of commands at your disposal.

In this section, I'll cover essential operations like stopping and starting your container, examining logs, and keeping your PostgreSQL version up to date.

### Stopping, restarting, and removing the PostgreSQL container

Docker's command-line tools allow you to manage the lifecycle of your PostgreSQL container.

To stop a running PostgreSQL container, run the following:

`docker stop postgres-db`

[](https://app.datacamp.com/workspace)

Similarly, run the following command when you need to start it back up:

`docker start postgres-db`

[](https://app.datacamp.com/workspace)

![Image 10 - Stopping and starting the container](https://media.datacamp.com/cms/ad_4nxdeoyuqmvhotk6j-pdzc2gsflhl-vwogbr1uqnes3hsdwyb81etvbd0l3iscpq7ndaqjwnipoa-hly0wmh1efy7s4qrgb4kbhh-jzel9mgq06fppnxzww8uw2yjyyg6lunjcopamq.png)

Image 10 - Stopping and starting the container

If you want to restart a running container, which can be useful after changing certain configurations, run the following command:

`docker restart postgres-db`

[](https://app.datacamp.com/workspace)

In cases when you're completely done with a container and want to remove it, look no further than these two commands:

`docker stop postgres-db docker rm postgres-db`

[](https://app.datacamp.com/workspace)

Remember that removing a container doesn't delete your data if you've set up a volume correctly. Your data will still be in the `postgres-data` volume created earlier.

You can verify the container has been removed by running:

`docker ps -a`

[](https://app.datacamp.com/workspace)

The `-a` flag shows all containers, including stopped ones. If your container was successfully removed, it won't appear in this list:

![Image 11 - Listing all containers](https://media.datacamp.com/cms/ad_4nxchhwfwevzgjl9z7kqgjklxqmuqjppfcklz2tyvgoe1tz_tezuhkmkkubefd5-qazo6uufwbzh74o7mh2ifn0mc3oehe7jasncejlrohyt0amyriljl8vqrusb_nfxwfacqlyw38g.png)

Image 11 - Listing all containers

### Inspecting the logs

When something goes wrong or you want to monitor your database activity, checking the logs is a good first step.

Run this command to view logs for your PostgreSQL container:

`docker logs postgres-db`

[](https://app.datacamp.com/workspace)

This shows all logs since the container started. For a large amount of logs, you might want to limit the output, let's say, to include just the last 50 logs:

`docker logs --tail 50 postgres-db`

[](https://app.datacamp.com/workspace)

![Image 12 - Viewing container logs](https://media.datacamp.com/cms/ad_4nxdzn6if0sqr48zqy4bsy00gj22zroo9vf0zbjwce56ifhrdua51fuvlefg3dqfln394e8kjhnrsdach74tnku88rv6cex67sfp1lgruzeveuborsy1dmp8h296pdtodet2w2w9epg.png)

Image 12 - Viewing container logs

On the other hand, if you want to follow the logs in real-time, this is the command you want to run:

`docker logs -f postgres-db`

[](https://app.datacamp.com/workspace)

![Image 13 - Viewing container logs in real time](https://media.datacamp.com/cms/ad_4nxef5kmb_v5q0y27fkhqxzepajrnmy_lxiklgmvihbm_ivp2eshpfmrisa-2wixq56_afmjml463zgy-u1majirbessrjlwcctabn8mmhlqad4_borad1ezgq6pak-nacq2_dsnwtq.png)

Image 13 - Viewing container logs in real time

This is particularly useful when debugging connection issues or watching database activity during development.

Press `Ctrl+C/CMD+C` to stop following the logs.

### Updating PostgreSQL in Docker

Over time, you'll want to update your PostgreSQL version to get the latest features, performance improvements, and security patches.

At the time of writing, `postgres:17.4` is the latest version, but let's theoretically assume `postgres:17.5` was released. This section will show you how to update the database version in your container.

To start, pull the latest PostgreSQL image (or a specific version):

`docker pull postgres:17.5`

[](https://app.datacamp.com/workspace)

Next, stop and remove the existing container:

`docker stop postgres-db docker rm postgres-db`

[](https://app.datacamp.com/workspace)

Finally, create a new container with the same volume:

`docker run --name postgres-db \   -e POSTGRES_PASSWORD=mysecretpassword \   -e POSTGRES_USER=myuser \   -e POSTGRES_DB=mydatabase \   -v postgres-data:/var/lib/postgresql/data \   -p 5432:5432 \   -d postgres:17.5`

[](https://app.datacamp.com/workspace)

Since you're using the same volume (`postgres-data`), all your existing data will be preserved.

If you're upgrading to a major new version (like 17 to 18), PostgreSQL will automatically run any necessary data migrations when it starts. Just keep these things in mind:

- Major version upgrades should be tested in a non-production environment first.
- Always back up your data volume before a major version upgrade.
- Check the PostgreSQL release notes for any breaking changes.

To create a backup before upgrading, run the following command:

`docker run --rm -v postgres-data:/data -v $(pwd):/backup postgres:17.4 \   bash -c "pg_dumpall -U myuser > /backup/postgres_backup.sql"`

[](https://app.datacamp.com/workspace)

This creates a SQL backup file in your current directory that you can use to restore your data if anything goes wrong.

_>You might find our [PostgreSQL Basics Cheat Sheet](https://www.datacamp.com/cheat-sheet/postgre-sql-basics-cheat-sheet) h_andy as a quick reference while working in Docker.

In the next section, I'll cover best practices for using PostgreSQL in Docker, including security considerations and optimization tips.

## Best Practices for Using PostgreSQL in Docker

The flexibility of Docker comes with responsibility. In this section, I'll share some best practices to make sure your containerized PostgreSQL setup is reliable, secure, and follows industry standards.

### Keep your data safe with regular backups

Regardless of how you run PostgreSQL, regular backups are a must-have. I've mentioned backups in the previous section, but this is where I'll kick it up a notch. 

The simplest way to back up a PostgreSQL database running in Docker is using `pg_dump`:

`docker exec -t postgres-db pg_dump -U myuser mydatabase > backup.sql`

[](https://app.datacamp.com/workspace)

![Image 14 - PostgreSQL backup](https://media.datacamp.com/cms/ad_4nxdeb6flwi-5x7h0r-y9bts01gebmm7l9hh7yp2tp9qvy4q8gxo4tvsabkefef9rppfmxvad43wnatzqmja9ml0kqx9emy80zpbut8krgyni_fs-pwr-zlibv4xzlysbrjp1du1ufq.png)

Image 14 - PostgreSQL backup

For a full backup of all databases, including roles and tablespaces, use `pg_dumpall`:

`docker exec -t postgres-db pg_dumpall -U myuser > full_backup.sql`

[](https://app.datacamp.com/workspace)

![Image 15 - Full PostgreSQL database backup](https://media.datacamp.com/cms/ad_4nxclbipqpwydsoqebtel0v_xt14lucxyj2au1gujjb6axpjfxls9sezwbhaf3ymyxzsl0gks7dopthungfonfivb1i25dahrzdzn4jjn0yxyk6ykhkqx6dqmhjotq0adbnz8vqlzyw.png)

Image 15 - Full PostgreSQL database backup

This image shows just a couple of backup commands, as fitting the entire thing to the screen isn't possible.

To automate your backups, you can create a simple shell script and run it with cron:

`#!/bin/bash # backup.sh TIMESTAMP=$(date +"%Y%m%d") BACKUP_DIR="/Users/dradecic/Documents/pg-backups"  # Make sure the backup directory exists mkdir -p $BACKUP_DIR  # Create the backup docker exec postgres-db pg_dumpall -U myuser | gzip > $BACKUP_DIR/postgres_$TIMESTAMP.sql.gz  # Remove backups older than 30 days find $BACKUP_DIR -name "postgres_*.sql.gz" -mtime +30 -delete`

[](https://app.datacamp.com/workspace)

Make the script executable and run it:

`chmod +x backup.sh  bash backup.sh`

[](https://app.datacamp.com/workspace)

![Image 16 - Running a PostgreSQL database backup script](https://media.datacamp.com/cms/ad_4nxcus39bjllrnjdggdli-fr0cu01eitfqjf_2yabvqzmik-pfpmzodu6jqoh5tkl9pwwg03aye_0gjunutccgn6rpicsudxbxajosxcwhuk8j7aawpbu3cns15vsqpnehk_jaqmskw.png)

Image 16 - Running a PostgreSQL database backup script

To fully automate the backup, you can add the script to your crontab to run daily:

`0 3 * * * /path/to/backup.sh`

[](https://app.datacamp.com/workspace)

This schedule runs the backup every day at 3 AM, but of course, you can adjust the timing and frequency as you need. 

>Check out my f_ull [guide on cron jobs](https://app.datacamp.com/learn/tutorials/cron-job-in-data-engineering) to_ learn more about this useful automation tool.

For production environments, consider storing backups off-site or in cloud storage for disaster recovery.

### Use named volumes for data persistence

While I covered volumes briefly earlier, it's worth reviewing them in more depth.

As a general rule, you should never run PostgreSQL in Docker without a properly configured volume. If you do, your data will be lost when the container is removed or when Docker performs cleanup operations.

Using named volumes (rather than anonymous volumes) makes data backup and management that much easier:

`# Create a named volume docker volume create postgres-data  # Use it when running the container docker run --name postgres-db \   -e POSTGRES_PASSWORD=mysecretpassword \   -v postgres-data:/var/lib/postgresql/data \   -d postgres`

[](https://app.datacamp.com/workspace)

Nothing new here.

Named volumes are also easier to back up. To create a backup of the entire volume, run the following command:

`docker run --rm -v postgres-data:/data -v $(pwd):/backup alpine tar czf /backup/postgres-data-backup.tar.gz /data`

[](https://app.datacamp.com/workspace)

This will create a `postgres-data-backup.tar.gz` file in the same folder from which you've executed the command.

Now, to restore this volume, run the following:

`docker run --rm -v postgres-data:/data -v $(pwd):/backup alpine sh -c "cd /data && tar xzf /backup/postgres-data-backup.tar.gz --strip 1"`

[](https://app.datacamp.com/workspace)

That's it!

### Securing PostgreSQL in Docker

When it comes to databases, security should never be an afterthought. This subsection will walk you through some essential practices for securing your PostgreSQL container.

#### Use strong and unique passwords

Avoid default or weak passwords. Generate a strong, random password for your PostgreSQL superuser:

`export POSTGRES_PASSWORD=$(openssl rand -base64 32) echo "$POSTGRES_PASSWORD" > postgres-password.txt  docker run --name postgres-db \   -e POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \   -v postgres-data:/var/lib/postgresql/data \   -d postgres`

[](https://app.datacamp.com/workspace)

![Image 17 - Using a secure password](https://media.datacamp.com/cms/ad_4nxedevx3bljyhwe_b4oq_hlq72dl8jhrhgwyriglgqywqow1uy2ucgsubqsflpw_zzibmiipr7xl7xlh9i3dekzqij0zydenabokv4ymrzea46cnz3bej6n5tnajsc_ppfvlvyiq-q.png)

Image 17 - Using a secure password

Store this password securely, such as in a password manager or environment variable file that's not checked into version control.

#### Restrict network access

By default, Docker exposes the PostgreSQL port on all interfaces. For improved security, especially in production, restrict access to localhost:

`docker run --name postgres-db \   -e POSTGRES_PASSWORD=mysecretpassword \   -p 127.0.0.1:5432:5432 \   -v postgres-data:/var/lib/postgresql/data \   -d postgres`

[](https://app.datacamp.com/workspace)

#### Use custom PostgreSQL configuration

Create a more secure PostgreSQL configuration by modifying parameters like the ones below:

`# Require SSL ssl = on ssl_cert_file = '/etc/ssl/certs/ssl-cert-snakeoil.pem' ssl_key_file = '/etc/ssl/private/ssl-cert-snakeoil.key'  # Limit connection attempts max_connections = 100 authentication_timeout = 1min  # Restrict access listen_addresses = 'localhost'`

[](https://app.datacamp.com/workspace)

Mount this configuration file when starting your container:

`docker run --name postgres-db \   -e POSTGRES_PASSWORD=mysecretpassword \   -v ./pg_hba.conf:/var/lib/postgresql/data/pg_hba.conf \   -v ./postgresql.conf:/var/lib/postgresql/data/postgresql.conf \   -v postgres-data:/var/lib/postgresql/data \   -d postgres`

[](https://app.datacamp.com/workspace)

#### Regularly update your PostgreSQL image

Keep your PostgreSQL version updated to get the latest security patches:

`docker pull postgres:latest docker stop postgres-db docker rm postgres-db # Then recreate with the latest image`

[](https://app.datacamp.com/workspace)

These best practices will allow you to create a more reliable and secure PostgreSQL environment in Docker that is suitable for both development and production use cases.

In the next section, I'll cover how to troubleshoot common issues you might face when running PostgreSQL in Docker.

## Troubleshooting PostgreSQL in Docker

Sooner or later, you're bound to run into issues when running PostgreSQL in Docker. I'll cover common problems and their solutions in this section, which will save you time and frustration along the way.

### Common issues with PostgreSQL containers

One common issue many users face is that their container exits immediately after starting. If that's the case for you, check the logs to identify the issue:

`docker logs postgres-db`

[](https://app.datacamp.com/workspace)

Your error could be tied to permission issues with mounted volumes. If that's the case, you'll see a similar log message:

`initdb: could not change permissions of directory "/var/lib/postgresql/data": Operation not permitted`

[](https://app.datacamp.com/workspace)

To solve this issue, check the ownership and permissions of your volume and then fix if needed:

`# Check the ownership docker run --rm -v postgres-data:/data alpine ls -la /data  # Fix the permissions docker run --rm -v postgres-data:/data alpine chmod 700 /data`

[](https://app.datacamp.com/workspace)

Another common issue is missing required environment variables. A typical log message when it happens looks like this:

`Database is uninitialized and superuser password is not specified`

[](https://app.datacamp.com/workspace)

To solve it, make sure you're setting the required `POSTGRES_PASSWORD` environment variable - or any other environment variable for that matter:

`docker run --name postgres-db \   -e POSTGRES_PASSWORD=mysecretpassword \   -v postgres-data:/var/lib/postgresql/data \   -d postgres`

[](https://app.datacamp.com/workspace)

The “Data directory not empty but missing PostgreSQL files” error is also common. This is the log message you're likely to see:

`PostgreSQL Database directory appears to contain a database; Skipping initialization`

[](https://app.datacamp.com/workspace)

Followed by errors about missing files.

This usually happens when you've mounted a volume that contains files but not a valid PostgreSQL database. You might need to reinitialize by using a new volume:

`docker volume create postgres-data-new docker run --name postgres-db \   -e POSTGRES_PASSWORD=mysecretpassword \   -v postgres-data-new:/var/lib/postgresql/data \   -d postgres`

[](https://app.datacamp.com/workspace)

### Resolving connectivity issues

If you can't connect to your PostgreSQL database running in a container, start by confirming the container is running:

`docker ps | grep postgres-db`

[](https://app.datacamp.com/workspace)

If it's not listed, it may have crashed. Check the logs as described earlier.

If it's listed but you're still unable to connect, verify port mapping:

`docker port postgres-db`

[](https://app.datacamp.com/workspace)

You should see something like this:

![Image 18 - Container port mapping](https://media.datacamp.com/cms/ad_4nxc2rrppgnistxhzxaeeylg0ywysitjhlvyarted1nso4wrz-je2luzn2orez1ud0ahvvrcwsnyl4ohlfh9ry6ibix_5s4gejrjz9g_e2zhlqhn_fstn_bzn6u_qw1sc_1uk09pu.png)

Image 18 - Container port mapping

If not, your port mapping may be incorrect. Recreate the container with the proper `-p` option.

If you still can't connect to the database, it's time to check your connection settings. Check these parameters:

- Hostname: `localhost` or `127.0.0.1` (not the container name).
- Port: The host port from your mapping (usually 5432).
- Username: The value of `POSTGRES_USER` (default is "postgres").
- Password: The value of `POSTGRES_PASSWORD`.
- Database: The value of `POSTGRES_DB` (default is same as `POSTGRES_USER`).

Try again after addressing these. If the issue still persists, you should test connectivity from inside the container:

`docker exec -it postgres-db psql -U postgres`

[](https://app.datacamp.com/workspace)

If this works, the issue is with your port mapping or external network.

Finally, you can check for firewall issues. Your system's firewall might be blocking connections to the PostgreSQL port, so give it a check:

`# Linux sudo iptables -L | grep 5432  # macOS sudo pfctl -sr | grep 5432`

[](https://app.datacamp.com/workspace)

By checking these common issues, you should be able to identify and resolve most problems with PostgreSQL in Docker. If you're still stuck, the PostgreSQL and Docker documentation and community forums are excellent resources for more specific troubleshooting.