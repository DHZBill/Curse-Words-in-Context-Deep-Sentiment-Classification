#tweet-analysis.py is a copy of the lambda function used for AWS cCmprehend

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
