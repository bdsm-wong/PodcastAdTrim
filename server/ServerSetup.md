# Server Setup

## Table of Contents
- [Preparing](#preparing)
- [Cloning/Updating Repository](#cloningupdating-repository)
- [Configuring the Environment](#configuring-the-environment)
- [Managing the Container](#managing-the-container)

## Preparing
1) Create or identify a top-level Docker projects directory on server
2) Install Docker
3) Open or identify a port to use for this service
4) Create or identify a directory to store audio matrix files.  
**Note: these files are not compressed, so will likely consume more space than the audio files themselves**

## Cloning/Updating Repository

Move to the top-level Docker projects directory from [Preparing](#preparing) step 1.  For example:`cd ~/Docker`

To clone entire repository  (only for the first time):
```bash
git clone https://github.com/bdsm-wong/PodcastAdTrim -b dev
```
* Automatically creates a directory for the project inside the present working directory.  
* For example: `~/Docker/PodcastAdTrim`
* `-b dev` clones the "dev" branch.  Omit to clone the default branch ("main").

To update the repository with changes (after initial cloning):
```bash
git pull
```
* This can be called from anywhere within the cloned repo directory.

## Configuring the Environment
* Move (as required) to where the example environment file is stored.  Using the example above, it will be here:
  * `~/Docker/PodcastAdTrim/server/.env.example`
* Copy `.env.example` as `.env`:
  * `cp .env.example .env`
* Edit the new .env file (for example, `nano .env`) and set the following variables:
  - `STORAGE_PATH`: Absolute path to store matrices of converted audios.
  - `NUM_PARTITIONS_CORRELATE` (Optional): Number of partitions in the source audio matrix. Default is 4.

[//]: # (TODO - review values and additional parameters)

## Managing the Container
Move (as required) to where the Docker `compose.yaml` file is stored.  `compose` commands below assume there is a file named `compose.yaml` in the present working directory.  Using the example above, it will be here:
* `~/Docker/PodcastAdTrim/server/compose.yaml`
### Start the container:
```bash
sudo docker compose up -d
```
  * Automatically builds all images and run the container
  * `-d` runs the container in 'detached' mode (in background).  Omit to leave in foreground.

### Stopping/removing the container:
```bash
sudo docker compose down --rmi all
```
* `--rmi all` removes all images associated with the container so they can be rebuilt from scratch.

### Show all images:

```bash
sudo docker images
```

### Check the status of containers:

```bash
sudo docker ps -a
```
* `-a` shows all processes (including stopped/faulted containers)

