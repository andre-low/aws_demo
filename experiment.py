import boto3 as aws
import time
from secrets import token_hex

# AWS setup
s3 = aws.client('s3')
transcribe = aws.client('transcribe')
translate = aws.client('translate')
polly = aws.client('polly')

# Variables
input_string = 'Take 2, 500mg tablets, of paracetemol, not more than 4 times a day.'
transcription_job_name = 'transcription_job_' + token_hex(3)

# Amazon Transcribe

# Start transcription job
transcribed_response_init = transcribe.start_medical_transcription_job(
    MedicalTranscriptionJobName = transcription_job_name,
    LanguageCode = 'en-US',
    MediaFormat = 'mp3',
    Media = {
        'MediaFileUri': 's3://andrelow.awsdemo.transcribe/aspirin.mp3'
    },
    OutputBucketName = 'andrelow.awsdemo.transcribe',
    Specialty = 'PRIMARYCARE',
    Type = 'DICTATION'
)

print(transcribed_response_init['MedicalTranscriptionJob'])
time.sleep(30)

# Get Uri of completed transcription job
transcribed_response_complete = transcribe.get_medical_transcription_job(
    MedicalTranscriptionJobName=transcription_job_name
)

print(transcribed_response_complete['MedicalTranscriptionJob']['Transcript']['TranscriptFileUri'])

""" # Amazon Translate
translated_response = translate.translate_text(
    Text = input_string,
    SourceLanguageCode='en',
    TargetLanguageCode='zh'
)

print(translated_response['TranslatedText'])

# Amazon Polly
speech_response = polly.synthesize_speech(
    OutputFormat = 'mp3',
    Text = translated_response['TranslatedText'],
    VoiceId = 'Zhiyu'
)

file = open('speech_response.mp3', 'wb')
file.write(speech_response['AudioStream'].read())
file.close() """