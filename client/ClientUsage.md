## Table of Contents
- [Testing Communications](#testing-communications)

## Testing Communications
Prior to setting up the client-side Python virtual environment, the server endpoints can be manually tested from the command line.

### Pinging the Server
```bash
ping myserver
```

### Endpoint 1: `/health`
```bash
curl http://myserver:port/health
```
* Replace `myserver` with the server's domain name.  Use `localhost` if calling from the server itself.
* Replace `port` with the port number configured in the `.env` file (refer to [server setup guide](server/ServerSetup.md)).
* This endpoint does not require any parameters.
* The reply will simply be `Healthy!` if the container is reachable.

### Endpoint 2: `/audio-detection`
#### Passing audio files directly (not stored matrix files)
```bash
curl -F "full_audio=@/path/to/file/myPodcast.mp3" -F "audio_fragment=@/path/to/file/myAd.mp3" http://myserver:port/audio-detection
```
* `/path/to/file/myPodcast.mp3` is the path (accessible from the client) to a full audio file.
* `/path/to/file/myAd.mp3` is the path to a partial audio file to locate within the full audio file.
* The `-F` switch emulates a filled-in form, which causes this to be treated as an HTTP `POST` request.
* The `@` symbols before the paths attach actual files to the `POST` request, rather than treating these as strings to be resolved by the server.
* If there are spaces in the file name(s), the path(s) must be wrapped in backslash-escaped double-quotes:
  * `"full_audio=@\"/path/to/file/myPodcast With Spaces.mp3\""`
* Paths relative to the present working directory can also be passed.  For example:
  * `"full_audio=myPodcast.mp3"`
  * `"full_audio=./subdir/myPodcast.mp3"`
* Refer to the [main README](#../Readme.md) for the expected response.

#### Referencing stored matrix files
```bash
curl -F "full_audio=myPodcast" -F "audio_fragment=myAd" http://myserver:port/audio-detection
```
* `myPodcast` refers to a file that has been stored as an audio matrix using the `/audio-storage` endpoint:
  * `myPodcast` must match the value of `name_audio` used when storing 
  * The file must have been stored using `"type_audio=full"`
  * The file will have the path `{STORAGE_PATH}/full/myPodcast.npz`
* Similarly, `myAd` must have been stored using `"type_audio=frag"` and will be found at `{STORAGE_PATH}/frag/myAd.npz`
* Note that the `@` symbols are omitted when referencing stored matrices. 
* Both parameters will accept either attached files or references to existing audio matrices.
* The response will be the same as when passing audio files directly.

### Endpoint 3: `/audio-storage`
#### Storing a full audio file
```bash
curl -F "name_audio=myPodcast" -F "file_audio=@/path/to/file/myPodcast.mp3" -F "type_audio=full" http://myserver:port/audio-storage
```
* The `file_audio` parameter works as described in [Passing audio files directly](#passing-audio-files-directly-not-stored-matrix-files)
* The file will be stored at `{STORAGE_PATH}/full/myPodcast.npz`
#### Storing a partial audio file
```bash
curl -F "name_audio=myAd" -F "file_audio=@/path/to/file/myAd.mp3" -F "type_audio=frag" http://myserver:port/audio-storage
```
* The file will be stored at `{STORAGE_PATH}/frag/myAd.npz`