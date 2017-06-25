# Movie-Translator-Bot

This sample requires a subscription with Microsoft Translator Speech Translation API, which is part of Microsoft Azure Cognitive Services. Visit the [Speech Translation API documentation page](http://docs.microsofttranslator.com/speech-translate.html) to get started.


## Setup
Samples are written for Python 2 and assume that `pip` is installed. Recent versions of Python 2.7 come with `pip`.

The [`requests`](http://docs.python-requests.org/en/master/) and [`websocket-client`](https://pypi.python.org/pypi/websocket-client) packages are required:

```
pip install requests
pip install websocket-client
```

## Getting list of supported languages (languages.py)
This sample demonstrates how to obtain the list of languages supported by the Speech Translation API. 

Run the example with:

```
python languages.py
```

## Movie Translate (movie_translate.py)
This sample demonstrates the use of Microsoft Translator Speech Translation API by translating an audio file.

Before running the example.

1. Fill your Azure Data Market Credentials

   ```client_secret = 'INSERT YOUR CLIENT SECRET'```

1. Fill in the name of your audio file (PCM, 16 bit, 16 kHz, mono, WAV)

    ```audio_file = 'INSERT AUDIO FILE FULL PATH'```

Run the example with:

```
python speech.py
```

## Getting an authentication token from the Azure platform (auth.py)
This class illustrates how to get an authentication token given a client secret. The client secret is the key associated with your Azure Cognitive Services subscription for the Speech Translation API. The value of the key is available in the Azure developer portal.

