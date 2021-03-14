import boto3 as aws
import time
import sys
import json
from secrets import token_hex


# AWS setup
s3 = aws.resource('s3')
transcribe = aws.client('transcribe')
translate = aws.client('translate')
polly = aws.client('polly')


# Variables
s3_bucket = ''
input_audio_file = ''
input_audio_s3_uri = 's3://' + s3_bucket + '/' + input_audio_file
transcription_job_name = 'transcription_job_' + token_hex(3)
output_file_name = 'output.mp3'


# Amazon Transcribe: start transcription job
print('Input audio retrieved from: ' + input_audio_s3_uri)

transcribed_response_init = transcribe.start_medical_transcription_job(
    MedicalTranscriptionJobName = transcription_job_name,
    LanguageCode = 'en-US',
    MediaFormat = 'mp3',
    Media = {
        'MediaFileUri': input_audio_s3_uri
    },
    OutputBucketName = s3_bucket,
    Specialty = 'PRIMARYCARE',
    Type = 'DICTATION'
)

for remaining in range(30, 0, -1):
    sys.stdout.write('\r')
    sys.stdout.write('Audio transcription in progress, {:2d} seconds remaining.'.format(remaining))
    sys.stdout.flush()
    time.sleep(1)


# Amazon Transcribe: fetch complete transcription to file and parse JSON
s3.meta.client.download_file(s3_bucket, 'medical/' + transcription_job_name + '.json', transcription_job_name + '.json')

with open('transcription.json') as f:
    transcription_response = json.load(f)

transcribed_text = transcription_response['results']['transcripts'][0]['transcript']

print('\rTranscribed text: ' + transcribed_text)


# Amazon Translate
translated_response = translate.translate_text(
    Text = transcribed_text,
    SourceLanguageCode='en',
    TargetLanguageCode='zh'
)

translated_text = translated_response['TranslatedText']

print('Translated text: ' + translated_text)


# Amazon Polly
speech_response = polly.synthesize_speech(
    OutputFormat = 'mp3',
    Text = translated_text,
    VoiceId = 'Zhiyu'
)

file = open(output_file_name, 'wb')
file.write(speech_response['AudioStream'].read())
file.close()

print('Output audio saved to: ' + output_file_name)