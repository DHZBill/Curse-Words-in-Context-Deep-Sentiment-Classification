# Detecting the Emotion Dynamics of Profanity Language In Social Media Through Time 
Repository for FA20 CS230 Final Project
*Authors: Haozheng Du, Wenxin Dong, Kezia Lopez*

# Overview
In this emotional analysis of  tweets containing curse words, we analyze the changes of emotional context of profanity through time. First, we build a multi-class emotion classifier using XLNET to classify sentiments of curse-word-contexts, and then use this trained  XLNET model to predict emotional context of archived tweets from 2011 to 2019. 

# Contents
This repository contains: 
Training data for our NLP model
Sampled Historical Tweets from 2011- 2019
Preprocessing Python scripts for the raw tweets
A Bert Model (abandoned due to low performance)
A XLNET Model 
Scripts to build and training the models
Script to predict using the models
Scripts for plotting trends in prediction data.

# Getting Started

## XLNET
This directory contains all files needed to train the XLNet model and perform data analysis on the historical tweet data. 
- Run *train_model.py* to train the XLNet model on *unique_tweets.csv*. Model weights are saved, and visualizations of model outputs are created.
- Run *predict_sentiment.py* to use the saved model weights to predict emotions on the historical tweet data.
- Run *interpret.py* to calculate data needed for plotting the graphs. 
- Run *plots.py* plot multi-line, bar, and pie charts that are useful for data-analysis. Plots auto-saved in */plots*. 

## lambda_results_analysis:
This directory contains a copy of the lambda function used for the AWS Comprehend Sentiment Analyzer as *lambda-function-copy.py*, the resulting predictions of sentiment by the AWS Comprehend model for the training set contained by *unique-tweets-test.json*, and the accuracy and results analysis portion in *comparison.py*.

## data_analysis:
This directory contains the cleaned csv file grabs for years 2011-2019. Additionally, it contains the directory archive_data_grabber. This directory contains the code used to download and process the archived historical Tweet data locally in biggrabber.py. Local_analysis is the directory to use when downloading day files locally (in the Archive Twitter Stream, day files are organized into small json file parcels). Local_analysis contains the preliminary local-analysis.py which parses through local Twitter data for curse words and writes them to local-*analysis-tweets.csv*. Biggrabber.py also uses *cleaner.py* in that same directory to clean tweets when processing them locally.

## training_data:
This directory contains *well_formatted.csv* which contains curse-word tweet grabs, and *unique_tweets.csv* which further cleans and removes duplicate tweets and is used as the training, validation, and test data for the XLNET model.


## getTweets.py
Use this script to grab tweets from the twitter API and auto-generate updated training set (*unique_tweets.csv*)

## cleanTweets.py
Use this script to clean, i.e. preprocess, raw training set (*unique_tweets.csv*). 
