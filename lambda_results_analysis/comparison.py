import json

'''
Sentiment numbers:
2 --> upset
0 --> encouraging
3 --> upset
1 --> upset
4 --> sarcastic

Comparison.py seeks to analyze the results of sentiment given by the AWS Comprehend service.
'''

#variables
wrong_encouraging_total = 0
wrong_upset_total = 0
wrong_encouraging = {}
wrong_upset = {}
sarcastic = {}
sarcastic_totals = {}
count_en = 0
count_up = 0
count_sar = 0

with open('unique-tweets-test.json') as json_file:
    data = json.load(json_file)
    total_tweets = 5763
    for t in data:
        #positive
        key = t["curseword"]
        if t["actual_sentiment"] == "0":
            count_en +=1
            if t["predicted_sentiment"]["Sentiment"] != "POSITIVE":
                wrong_encouraging_total += 1
                if key not in wrong_encouraging:
                    wrong_encouraging[key] = 0
                wrong_encouraging[key] += 1
        #negative
        if t["actual_sentiment"] == "1" or t["actual_sentiment"] == "2" or t["actual_sentiment"] == "3":
            count_up += 1
            if t["predicted_sentiment"]["Sentiment"] != "NEGATIVE":
                wrong_upset_total += 1
                if key not in wrong_upset:
                    wrong_upset[key] = 0
                wrong_upset[key] += 1
        if t["actual_sentiment"] == "4":
            if key not in sarcastic:
                sarcastic[key + t["predicted_sentiment"]["Sentiment"]] = 0
            pred = t["predicted_sentiment"]["Sentiment"]
            if pred not in sarcastic_totals:
                sarcastic_totals[pred] = 0
            sarcastic[key + t["predicted_sentiment"]["Sentiment"]] += 1
            sarcastic_totals[pred] += 1
            count_sar +=1

    print("Wrong encouraging tweet total: ", wrong_encouraging_total)
    print("Wrong encouraging breakdown: ", wrong_encouraging)
    print("Wrong upset tweet total: ", wrong_upset_total)
    print("Wrong upset breakdown: ", wrong_upset)
    #comprint("Sarcastic breakdown: ", sarcastic)
    print("Sarcastic total breakdown", sarcastic_totals)
    print("overall ratio tweets classified incorrectly: ", (wrong_encouraging_total+wrong_upset_total)/total_tweets)
    print("ratio encouraging tweets classified incorrectly", wrong_encouraging_total/count_en)
    print("ratio upset tweets classified incorrectly", wrong_upset_total/count_up)





