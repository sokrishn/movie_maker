"""
Python sample demonstrating use of Microsoft Translator Speech Translation API.
"""

import os
import StringIO
import struct
import thread
import time
import uuid
import wave
import sys
import subprocess
import websocket

from auth import AzureAuthClient
from subprocess import call

def get_wave_header(frame_rate):
    """
    Generate WAV header that precedes actual audio data sent to the speech translation service.

    :param frame_rate: Sampling frequency (8000 for 8kHz or 16000 for 16kHz).
    :return: binary string
    """

    if frame_rate not in [8000, 16000]:
        raise ValueError("Sampling frequency, frame_rate, should be 8000 or 16000.")

    nchannels = 1
    bytes_per_sample = 2

    output = StringIO.StringIO()
    output.write('RIFF')
    output.write(struct.pack('<L', 0))
    output.write('WAVE')
    output.write('fmt ')
    output.write(struct.pack('<L', 18))
    output.write(struct.pack('<H', 0x0001))
    output.write(struct.pack('<H', nchannels))
    output.write(struct.pack('<L', frame_rate))
    output.write(struct.pack('<L', frame_rate * nchannels * bytes_per_sample))
    output.write(struct.pack('<H', nchannels * bytes_per_sample))
    output.write(struct.pack('<H', bytes_per_sample * 8))
    output.write(struct.pack('<H', 0))
    output.write('data')
    output.write(struct.pack('<L', 0))

    data = output.getvalue()

    output.close()

    return data


class WaveFileAudioSource(object):
    """
    Provides a way to read audio from the DATA section of a WAV file in chunks of
    a specified duration.
    """

    def __init__(self, path, chunk_length, silence_duration):
        """
        :param path: Path to WAV file. Acceptable WAV files use PCM single channel
            with 16-bit samples and sampling frequency of 8 kHz or 16 kHz.
        :param chunk_length: Length of chunk in milliseconds. The chunk length should
            be a multiple of 10ms and in the range from 100ms to 1000ms.
        :param silence_duration: Optionally follow audio from the file with silence.
            Speech recognizer uses silence to find end of utterances. Silence duration
            is given in milliseconds.
        """

        self.input = wave.open(path, 'rb')

        if self.input.getnchannels() != 1:
            raise ValueError("Input audio file should have a single channel.")
        if self.input.getframerate() not in [8000, 16000]:
            raise ValueError("Input audio file should have sampling frequency of 8 or 16 kHz.")
        if self.input.getsampwidth() != 2:
            raise ValueError("Input audio file should have 16-bit samples.")
        if chunk_length % 10 != 0 or chunk_length < 100 or chunk_length > 1000:
            raise ValueError("Chunk length is too small, too large or not a multiple of 10 ms.")

        self.chunk_length = chunk_length
        self.chunk_size = int(self.input.getframerate() / (1000.0 / chunk_length))
        self.silence_duration = silence_duration
        self.silence_chunk = [0] * (2 * self.chunk_size)
        self.eof_reached = False

    def getframerate(self):
        return self.input.getframerate()

    def close(self):
        self.input.close()

    def __iter__(self):
        return self

    def next(self):
        if not self.eof_reached:
            data = self.input.readframes(self.chunk_size)
            if len(data) > 0:
                return data
            self.eof_reached = True
        if self.silence_duration > 0:
            self.silence_duration -= self.chunk_length
            return self.silence_chunk
        raise StopIteration


if __name__ == "__main__":

    #client_secret = 'INSERT YOUR CLIENT SECRET'
    #client_secret = '503e74c2ec0342d2bb3f891d7b5a1bf0'

    client_secret = input("Enter Microsoft Azure Cognitive API Services Key : ")
    mp4_file = input("Enter the location (Full Path) of the Movie file (MP4) : ")

    filename, file_extension = os.path.splitext(mp4_file)
    muted_source_file = filename + "-muted.mp4" 
    audio_mp3_file =  filename + ".mp3"
    audio_wav_file =  filename + ".wav"

    print("""
    Select the Language of the original movie 
        1.English
        2.French
        3.Spanish
        4.German
        5.Italian
        6.Portuguese
        7.Russian
    """)

    from_l = input("[1-7] : ")

    if (from_l == 1):
        translate_from = 'en-US'
        from_language = "English"
    elif (from_l == 2):
        translate_from = 'fr'
        from_language = "French"
    elif (from_l == 3):
        translate_from = 'es'
        from_language = "Spanish"
    elif (from_l == 4):
        translate_from = 'de'
        from_language = "German"
    elif (from_l == 5): 
        translate_from = 'it'
        from_language = "Italian"
    elif (from_l == 6): 
        translate_from = 'pt'
        from_language = "Portugese"
    elif (from_l == 7): 
        translate_from = 'ru'
        from_language = "Russian"
    else: 
        print("Don't know how to translate from this language")
        exit

    print("""
     Select the language you want me to translate this movie to 
        1.English
        2.French
        3.Spanish
        4.German
        5.Italian
        6.Portuguese
        7.Russian
    """)

    to_l = input("[1-7] : ") 

    if (to_l == 1):
        translate_to = 'en-US'
        to_language = "English"
    elif (to_l == 2):
        translate_to = 'fr'
        to_language = "French"
    elif (to_l == 3):
        translate_to = 'es'
        to_language = "Spanish"
    elif (to_l == 4):
        translate_to = 'de'
        to_language = "German"
    elif (to_l == 5): 
        translate_to = 'it'
        to_language = "Italian"
    elif (to_l == 6): 
        translate_to = 'pt'
        to_language = "Portugese"
    elif (to_l == 7): 
        translate_to = 'ru'
        to_language = "Russian"
    else:
        print("Don't know how to translate to this language")
        exit

    #client_secret = '99206079bfb44ec89ffbbdf1243ed521'
    auth_client = AzureAuthClient(client_secret)

    #Audio file(s) to transcribe
    #audio_file = 'INSERT AUDIO FILE FULL PATH'
    #audio_file = '/Users/sowkrish/Downloads/Lost-S1E1.wav'
    #audio_file = '/Users/sowkrish/Downloads/Crouching-Tiger-1.wav'
    #audio_file = '/Users/sowkrish/Downloads/Lion_Mountain_Lion_Mavericks_Yosemite_El-Captain_15.05.2017/Crouching-Tiger.wav'
    #audio_file = '/Users/sowkrish/Downloads/intouchables.wav'

    time.sleep(1)
    print("Extracting the Muted Video from original movie using ffmpeg.")
    call(["ffmpeg", "-i", mp4_file, "-vcodec", "copy", "-an", muted_source_file])

    time.sleep(1)
    print(" ")
    print("Extracting the Audio from the original movie using ffmpeg.")
    call(["ffmpeg", "-i", mp4_file, audio_mp3_file])
    call(["ffmpeg", "-i", audio_mp3_file, "-acodec", "pcm_s16le", "-ac", "1", "-ar", "16000", audio_wav_file])
    time.sleep(1)
    print(" ")

    audio_source = WaveFileAudioSource(audio_wav_file, 100, 2000)

    # Translate from this language. The language must match the source audio.
    # Supported languages are given by the 'speech' scope of the supported languages API.

    #translate_from = 'en-US'
    #translate_from = 'zh-CHS'
    #translate_from = 'fr'

    # Translate to this language.
    # Supported languages are given by the 'text' scope of the supported languages API.
    # translate_to = 'fr'
    # translate_to = 'en-US'
    # Features requested by the client.
    features = "Partial,TextToSpeech,TimingInfo"

    # Transcription results will be saved into a new folder in the current directory
    output_folder = os.path.join(os.getcwd(), uuid.uuid4().hex)

    # These variables keep track of the number of text-to-speech segments received.
    # Each segment will be saved in its own audio file in the output folder.
    tts_state = {'count': 0}

    # Setup functions for the Websocket connection

    def on_open(ws):
        """
        Callback executed once the Websocket connection is opened.
        This function handles streaming of audio to the server.

        :param ws: Websocket client.
        """

        print 'Connected. Server generated request ID = ', ws.sock.headers['x-requestid']

        def run(*args):
            """Background task which streams audio."""

            # Send WAVE header to provide audio format information
            data = get_wave_header(audio_source.getframerate())
            ws.send(data, websocket.ABNF.OPCODE_BINARY)
            # Stream audio one chunk at a time
            for data in audio_source:
                sys.stdout.write('.')
                ws.send(data, websocket.ABNF.OPCODE_BINARY)
                time.sleep(0.1)

            audio_source.close()
            ws.close()
            print 'Background thread terminating...'

        thread.start_new_thread(run, ())

    def on_close(ws):
        """
        Callback executed once the Websocket connection is closed.

        :param ws: Websocket client.
        """
        print 'Connection closed...'

    def on_error(ws, error):
        """
        Callback executed when an issue occurs during the connection.

        :param ws: Websocket client.
        """
        print error

    def on_data(ws, message, message_type, fin):
        """
        Callback executed when Websocket messages are received from the server.

        :param ws: Websocket client.
        :param message: Message data as utf-8 string.
        :param message_type: Message type: ABNF.OPCODE_TEXT or ABNF.OPCODE_BINARY.
        :param fin: Websocket FIN bit. If 0, the data continues.
        """

        if message_type == websocket.ABNF.OPCODE_TEXT:
            print '\n', message, '\n'
        else:
            tts_count = tts_state['count']
            tts_file = tts_state.get('file', None)
            if tts_file is None:
                tts_count += 1
                tts_state['count'] = tts_count
                fname = "tts_{0}.wav".format(tts_count)
                print "\nTTS segment #{0} begins (file name: '{1}').\n".format(tts_count, fname)
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                tts_file = open(os.path.join(output_folder, fname), 'wb')
                tts_state['file'] = tts_file
            tts_file.write(message)
            if fin:
                print '\n', "TTS segment #{0} ends.'.".format(tts_count), '\n'
                tts_file.close()
                del tts_state['file']

    client_trace_id = str(uuid.uuid4())
    request_url = "wss://dev.microsofttranslator.com/speech/translate?from={0}&to={1}&features={2}&api-version=1.0".format(translate_from, translate_to, features)

    print "Ready to connect..."
    print "Request URL      = {0})".format(request_url)
    print "ClientTraceId    = {0}".format(client_trace_id)
    print 'Results location = %s\n' % (output_folder)

    time.sleep(1)
    print(" ")
    print("Translating the Audio from " + from_language + " to " + to_language)
    time.sleep(1)
    print(" ")
    print("This will take a few minutes ...")

    saved_stdout = sys.stdout

    f = open("log-file", "w")
    sys.stdout = f

    ws_client = websocket.WebSocketApp(
        request_url,
        header=[
            'Authorization: Bearer ' + auth_client.get_access_token(),
            'X-ClientTraceId: ' + client_trace_id
        ],
        on_open=on_open,
        on_data=on_data,
        on_error=on_error,
        on_close=on_close
    )
    ws_client.run_forever()
    f.close()
   
    sys.stdout = saved_stdout 
    print(" ")
    print("Translation of Audio from " + from_language + " to " + to_language + " Complete!")
    time.sleep(1)
    print(" ")
    print("Remixing of the Muted Video with Translated Audio")
    time.sleep(1)
    print(" ")
    print("Movie Ready for viewing in " + to_language + ", Enjoy your Movie! ") 
    print(" ")
