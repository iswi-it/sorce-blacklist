# SOrCE Blacklist

Application to share blacklisted participants among SOrCE conferences in a data-privacy conform way. Private and identifiable data of blacklisted participants is stored as hash values in a database. Users can make requests to this database using hash values to check if full or partial data of this participant is stored in the blacklist. Hashes will be created in the frontend, so that the database and backend never see any private data of the participant.

## Setup

To setup the application, only a docker instance with docker-compose is required. It is recommended to run it behind a web proxy.

After cloning the repository, please edit the file `backend.env.example` with your initial user and a newly generated secret key (use `openssl rand -hex 32`). Afterwards rename it to `backend.env`.

    mv backend.env.example backend.env

Now you can start the containers using:

    docker-compose up -d

It will run the backend on port `8000`. If you would like to change this, you can edit the docker-compose file.