from boto3 import Session
from contextlib import closing
import os
import sys

# Create a client using the credentials and region defined in the [adminuser]
# section of the AWS credentials file (~/.aws/credentials).
session = Session(profile_name="default")
polly = session.client("polly")

audio_Id = 0
output_target = os.path.join( os.path.dirname(os.path.abspath(__file__)), "..", "out", "tmp", "audio" )

def speak ( text, is_nsfw ):
    
    global audio_Id
    audio_Id += 1
    voice = "Salli" if is_nsfw else "Matthew"
    response = polly.synthesize_speech( Text=text, OutputFormat="mp3", VoiceId=voice, Engine = 'neural' )

    with closing(response["AudioStream"]) as stream:

        output = os.path.join( output_target, str(audio_Id) + ".mp3" )
        with open(output, "wb") as file:
            file.write(stream.read())

    return str(audio_Id)

def get_processedStream ( stream, is_nsfw ) :

    title, streams = stream
    output = [] 

    def process( comment ) :
        return [ speak(phrase, is_nsfw) for phrase in comment if len(phrase) != 0]
    
    for stream in streams :

        tts_ids = []

        for comment in stream :
            tts_ids.append( process(comment) )

        output.append( tts_ids )
    
    title = process(title)

    global audio_Id
    audio_Id = 0
    return ( title , output )