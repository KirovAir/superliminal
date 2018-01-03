Superliminal
==========
Small http app for [Subliminal](https://github.com/Diaoul/subliminal) subtitle downloader to use with [Sonarr](https://github.com/Sonarr/Sonarr) / [Radarr](https://github.com/Radarr/Radarr) webhooks.

## Why?
When you don't want to touch/alter the official Docker images of Sonarr / Radarr it's impossible to neatly integrate Subliminal next to those as another container. (At least without dirty container privilege haxx)
This is simply a small webservice on top of the official Subliminal container which listens for Sonarr / Radarr webhook requests and then runs Subliminal on the downloaded file accordingly. 

#### Some limitions
- This will not pro-actively search for subtitles afterwards. It's a simple fix to use Subliminal in a Docker container too and never intended to be more. 
- For best results movie/series files should not be renamed. 

## Installation
- Setup this [Docker container](https://hub.docker.com/r/kirovair/superliminal/) next to your other Sonarr / Radarr container(s). 
- Make sure you map the /config volume to something you can access. **Also map your video folders EXACTLY the same way you have in your Sonarr / Radarr containers.** (Ex: /videos /tv /anime should be accessible using the same volume paths!)
- Run the superliminal container and edit arguments.txt (found in /config) accordingly. 
- Add the webhook in Sonarr / Radarr

#### Example of arguments.txt
```
{
    "default": "--cache-dir /config --addic7ed YOURUSERNAME YOURPASSWORD --opensubtitles YOURUSERNAME YOURPASSWORD download -p addic7ed -p opensubtitles -l nl -m 85 -v \"#FILE#\"",
    "sonarr": null,
    "radarr": null
}
```

Then `#FILE#` will be replaced with the complete filepath of a tv show of movie after downloading.
If you want different Subliminal parameters for Sonarr or Radarr use the corresponding values accordingly. The `default` parameters will be used when `sonarr` / `radarr` is null.

#### Add a webhook in Radarr/Sonarr
Go in Settings to configure a "Connect" WebHook:

- Settings &gt; Connect &gt; add WebHook notification
- Select **On Download** and **On Upgrade**
- URL: `http://<ip address>:<port>/`
- Example: `http://192.168.2.2:8978/`
- Method: POST

## Contribute
This was intended for personal use and it 'works-for-me &trade;' so just shoot a pull request / issue if you see room for improvement. Tested on a Synology DS216+II with 8GB RAM.

#### Troubleshooting
Check the logs in /config for any pointers on what is wrong. :D
