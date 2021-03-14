import json

with open('transcription_job_1d9026.json') as f:
  data = json.load(f)

print(data['results']['transcripts'][0]['transcript'])