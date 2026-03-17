# Steps to Set Up and Run Docker Container
**Cloning/Updating Repository**

Move to the Docker directory:
```bash
cd ~/Docker
```

Need to clone entire repository  (only for the first time):
```bash
git clone https://github.com/bdsm-wong/PodcastAdTrim -b dev
```
* `-b dev` clones the "dev" branch.  Omit to clone the default branch ("main").

To update the repository with changes (after initial cloning):
```bash
git pull
```
* Can call from anywhere within the cloned repo directory.

**Starting the Container**

```bash
cd PodcastAdTrim
sudo docker compose up -d
```
* `-d` runs the container in 'detached' mode (in background).  Omit to leave in foreground.
* Must call `compose` from root directory of repo (same location as compose.yaml file).

Show all images:

```bash
sudo docker images
```

Check the status of containers using:

```bash
sudo docker ps -a
```
* `-a` shows all processes (including stopped/faulted containers)

**Stopping/Removing the Container**

```bash
sudo docker compose down --rmi all
```
* Must call `compose` from root directory of repo (same location as compose.yaml file).
* `--rmi all` removes all images associated with the container so they can be rebuilt from scratch.

# Audio Detection Service

The **Audio Detection Service** is a Python-based utility designed to pinpoint the precise moment when a second audio snippet, extracted or recorded from a larger audio source, is played. Whether it's a snippet from a song, movie, video, or any other audio content, this service aims to determine the exact timestamp in the original audio where the provided snippet was played.

## Table of Contents
- [Getting Started](#getting-started)
    - [Introduction](#introduction)
    - [Installation](#installation)
        - [Install Dependencies](#install-dependencies)
        - [Configure Audio File Formats](#configure-audio-file-formats)
        - [Create .env File](#create-env-file)
        - [Configure Deployment Port](#configure-deployment-port)
        - [Run the Service](#run-the-service)
- [How it Works](#how-it-works)
- [What the Service Offers](#what-the-service-offers)
    - [Endpoint 1: `/audio-detection`](#endpoint-1-audio-detection)
    - [Endpoint 2: `/audio-storage`](#endpoint-2-audio-storage)
    - [Optional Variables](#optional-variables)
        - [Validating the Audio Fragment](#validating-the-audio-fragment)
        - [Variable for Displaying Content](#variable-for-displaying-content)
        - [Example: Optional Variables](#example-optional-variables)
        - [Example Response: Optional Variables](#example-response-optional-variables)
        - [Create .env File](#create-env-file)

## Getting Started
### Introduction

Welcome to AudioTimestamp-Detective – a Python-based audio analysis service designed to precisely locate the moment a specific audio fragment occurs within a larger audio source. Whether you're working with music, movies, or any audio content, this service simplifies the process of identifying when a particular sound occurs.

**Key Features:**
1. **Precision Detection**: Quickly find the exact second when a specific audio fragment is present.
2. **Flexible Endpoints**: Two endpoints cater to various use cases, from real-time detection to stored audio analysis.
3. **Optional Parameters**: Fine-tune your analysis with optional variables for enhanced accuracy.
4. **Easy Integration**: Seamlessly integrate this service into your applications using simple HTTP requests.

### Installation
To set up AudioTimestamp-Detective, follow these steps:

#### Install Dependencies
```bash
pip3 install -r requirements.txt
```
Make sure you are using `Python3` and `pip3`. Additionally, ensure that the version of librosa in requirements.txt is the specified version or higher.

#### Configure Audio File Formats
- For `GNU/Linux` systems, install ffmpeg and upgrade librosa for audio formats (.mp3, .wav, .m4a):
    ```bash
    sudo apt install ffmpeg
    pip3 install --upgrade librosa
    ```
- For macOS or Windows, you might need to install ffmpeg.

#### Create .env File
- Copy .env.example and create a .env file. Set the following variables:
    - `STORAGE_PATH`: Absolute path to store matrices of converted audios.
    - `NUM_PARTITIONS_CORRELATE` (Optional): Number of partitions in the source audio matrix. Default is 4.

#### Configure Deployment Port
Edit main.py to set the desired deployment port. You can configure the service for deployment with Apache, Nginx, or Gunicorn.

#### Run the Service
Execute the following command to start the service:
```bash
python3 main.py
```
Make HTTP requests to the endpoints: http://domain:port/endpoint.
## How it Works

1. **Audio Source**: You provide a complete audio file, representing the entire sound source, such as a song, movie, or video.

2. **Audio Fragment**: You obtain a fragment of audio either by recording it or extracting it from the source. This fragment could be captured using a mobile device or manually trimmed.

3. **Detection**: The service utilizes correlation techniques, dividing the audio matrix into partitions to enhance computational efficiency. By analyzing the provided fragment against the original audio, the system identifies the exact moment in the source where the fragment was played.

## What the Service Offers

The **Audio Detection Service** provides three endpoints accessible through `POST` requests, each serving a specific purpose:

### Endpoint 1: `/audio-detection`

This endpoint is responsible for finding the exact moment a specific audio fragment is played within a more extensive audio source. The required parameters are:

- `full_audio`: The complete audio to be analyzed for the specific moment. (Accepted formats: .mp3, .m4a, .ogg, .wav)
- `audio_fragment`: The audio fragment whose position is being sought. (Accepted formats: .mp3, .m4a, .ogg, .wav)

**Response:**
The response is a numeric value representing the time in seconds where the highest correlation was detected, i.e., the exact moment the audio fragment was played.
```json
{
    "error": false,
    "message": {
        "location_in_seconds": 120.26713435374151
    }
}
```

### Endpoint 2: `/audio-storage`

This endpoint stores a full or partial audio file on the server for future queries. The required parameters are:

- `type_audio`: 'frag' if this is a snippet/partial file or 'full' if this is the full audio clip (Type: String)
- `name_audio`: A unique name for the audio to be stored in the system. (Type: String)
- `file_audio`: The complete audio to be saved in the system for later analysis. (Accepted formats: .mp3, .m4a, .ogg, .wav)

**Response:**
The response confirms the successful file storage on the server.
```json
{
    "error": false,
    "message": "Audio matrix saved successfully"
}
```


### Optional Variables

Both Endpoint 1 and 3 accept optional variables for directly validating the audio fragment and showing additional result data.

#### Validating the Audio Fragment

These variables allow validation of the audio fragment, including duration and amplitude averages:

- `recorded_fragment_duration_min`: Should be an integer or float, representing the minimum duration (in seconds) allowed for the audio fragment.
- `recorded_fragment_duration_max`: Should be an integer or float, representing the maximum duration (in seconds) allowed for the audio fragment.
- `min_average_fragment_amplitude`: Should be a float between 0 and 1, indicating the minimum average amplitude required for the audio fragment.
- `max_average_fragment_amplitude`: Should be a float between 0 and 1, indicating the maximum average amplitude allowed for the audio fragment.

#### Variable for Displaying Content

- `show`: This variable is a list that determines what data will be included in the response. You can include the following elements based on your requirements:
  - `location_in_seconds`: Time in seconds where the highest correlation was detected.
  - `total_execution_time`: Total time taken for the operation.
  - `location_in_minutes`: Time in minutes and seconds where the highest correlation was detected.
  - `recorded_fragment_length`: Duration of the audio fragment.
  - `fragment_average_amplitude`: Average amplitude of the audio fragment.

#### Example: Optional Variables
```json
{
  "show": ["location_in_seconds", "total_execution_time", "location_in_minutes"],
  "recorded_fragment_duration_min": 5,
  "recorded_fragment_duration_max": 30,
  "min_average_fragment_amplitude": 0.002,
  "max_average_fragment_amplitude": 0.8
}
```

#### Example Response: Optional Variables
```json
{
    "error": false,
    "message": {
        "fragment_average_amplitude": 0.007715221613379777,
        "location_in_minutes": "2:0.27",
        "location_in_seconds": 120.26713435374151,
        "recorded_fragment_length": 20.735714285714284,
        "total_execution_time": 1.173021125793457
    }
}
```