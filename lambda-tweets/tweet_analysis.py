'''
TEST CSV WRITER
import csv

with open('testcsv.csv', mode='w') as test:
    writer = csv.writer(test, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    writer.writerow(['text', 'curseword', 'curseWordCatg', 'date'])
    writer.writerow(["userid fuck those people. so dumb. ", 'fuck', '7', 'Oct2011'])
    writer.writerow(["if they were worth shit they'd understand that people not dying ", 'shit', '3', 'Oct2011'])
    writer.writerow(["that nigga sucks ", 'nigga', '3', 'Oct2011'])
    writer.writerow(["bitches be hating. i am bitches ", 'bitch', '1', 'Oct2011'])
'''
import json
import csv
   
key = 't1.csv'
temp = [{'greetings': "hello", "affirmations": "yup", "neins": "no"}, 
{'greetings': "hello", "affirmations": "yup", "neins": "no"},
{'greetings': "hello", "affirmations": "yup", "neins": "no"}]
filename = "unique-tweets-test" + ".json"

j = json.dumps(temp).encode('utf-8')
print(j)
print("put complete!")

'''
import json
import boto3
import csv

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    
    bucket = 'tweets-over-time'
    key = 'testcsv.csv'

    f = s3.get_object(Bucket=bucket, Key=key)
    raw = f['Body']
    return(type(raw))
    #.read().decode("utf-8")
    csv_reader_object = csv.reader(raw, delimiter="\n")
    
    comprehend = boto3.client("comprehend")
    for row in csv_reader_object:
        print("CSV row: {0}".format(row))
        print(comprehend.detect_sentiment(Text= row[0], LanguageCode = "en"))


   


    return rows
'''




'''
import json
import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    
    bucket = 'tweets-over-time'
    key = 'testcsv.csv'

    f = s3.get_object(Bucket=bucket, Key = key)
    paragraph = str(f["Body"].read)

    comprehend = boto3.client("comprehend")
    response = comprehend.detect_sentiment(Text= paragraph, languageCode = "en")

    print(response)

    return "hello from lambda"

'''






'''
FINAL
import json
import boto3

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    try:
        response = s3.get_object(Bucket=bucket, Key=key)

        text = response["Body"].read().decode()
        print(text)

    except Exception as e:
        print(e)
        raise(e)
'''
'''
FIRST VERSION:

import json
import boto3

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket = 'tweets-over-time'

    if event:
        print("Event: ", event)
        file_obj = event["Records"][0]
        filename = str(file_obj['s3']['object']['key'])
        print("Filename: ", filename)
        
        fileObj = s3.get_Object(Bucket='tweets-over-time', Key='file-name')
        file_content = fileObj["Body"].read().decode('utf-8')
        print(file_content)

    return("yuh")
'''
