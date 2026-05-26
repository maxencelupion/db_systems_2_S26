# DB Systems 2 S26
This repository contains the code for the DB Systems 2 S26 pre exam.

We chose the 'Standard project', aiming to create a database usable for a chat system.

# How to run
To run the application, you can either use Docker or run the application locally.

## Docker
To run the application using Docker, follow these steps:
We assume you have Docker & Docker compose installed on your machine.

1. Clone the repository: `git clone https://github.com/maxencelupion/db_systems_2_S26.git`
2. Navigate to the repository directory: `cd db_systems_2_S26`
3. Build the Docker image: `docker compose up --build -d`
4. Run the Docker container for the first time to create the tables: `docker compose run --rm app prisma db push`
5. Run the Docker container: `docker compose run --rm -it app`. `-it` allows you to interact with the container's terminal.

## Local
1. Clone the repository: `git clone https://github.com/maxencelupion/db_systems_2_S26.git`
2. Navigate to the repository directory: `cd db_systems_2_S26`
3. Install the dependencies: `pip install -r requirements.txt`
4. Create the `.env` file: `cp .env.example .env` and fill in the required environment variables.
5. Create the tables: `prisma db push`
6. Run the application: `python3 src/main.py `
