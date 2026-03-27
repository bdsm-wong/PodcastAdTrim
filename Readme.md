
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
      - [Endpoint 1: `/health`](#endpoint-1-health) 
      - [Endpoint 2: `/audio-detection`](#endpoint-2-audio-detection)
      - [Endpoint 3: `/audio-storage`](#endpoint-3-audio-storage)
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
To set up PodcastAdTrim on a server, follow the [server setup guide](server/ServerSetup.md).

To install and use client-side tools, follow the [client usage guide](client/ClientUsage.md)

## How it Works

1. **Audio Source**: You provide a complete audio file, representing the entire sound source, such as a song, movie, or video.

2. **Audio Fragment**: You obtain a fragment of audio either by recording it or extracting it from the source. This fragment could be captured using a mobile device or manually trimmed.

3. **Detection**: The service utilizes correlation techniques, dividing the audio matrix into partitions to enhance computational efficiency. By analyzing the provided fragment against the original audio, the system identifies the exact moment in the source where the fragment was played.

## What the Service Offers

The **Audio Detection Service** provides three endpoints accessible through `POST` requests, each serving a specific purpose:

### Endpoint 1: `/health`

* This endpoint is used periodically by the Docker Flask service to verify that the network is available.  
* Refer to [client usage guide](client/ClientUsage.md) for ad-hoc usage.

### Endpoint 2: `/audio-detection`

This endpoint is responsible for finding the exact moment a specific audio fragment is played within a more extensive audio source. The required parameters are:

- `full_audio`: The complete audio to be analyzed for the specific moment.
  - Can pass file or path to cached data. 
  - If passing a file, accepted formats are: .mp3, .m4a, .ogg, .wav
  - Cached data is stored in `full` directory of volume referenced in `STORAGE_PATH` environment variable.
  - For example, if path to file is: `{$STORAGE_PATH}/full/myFile.npz`, use `myfile` for this argument.  
- `audio_fragment`: The audio fragment whose position is being sought.
  - Like with `full_audio`, can pass file or path.  However, cached files are in the `frag` directory.  

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

### Endpoint 3: `/audio-storage`

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