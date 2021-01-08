# -*- coding: utf-8 -*-
import csv
import datetime
import boto3
import json
from django.core.management.base import BaseCommand, CommandError
from meal.models import MealType, MealMenu, AwsSentimentAnalysis

# AWS region
REGION = 'ap-northeast-1'

class Command(BaseCommand):

    # Function for detecting sentiment
    def detect_sentiment(self, text, aws_access_key_id, aws_secret_access_key, language_code):
        comprehend = boto3.client(
            'comprehend',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=REGION
        )
        response = comprehend.detect_sentiment(Text=text, LanguageCode=language_code)
        return response

    def handle(self, *args, **options):

        # Meal dataset 
        meal_dataset = MealMenu.objects.all()
   
        # language code
        language_code = 'ja'

        # aws credential
        aws_cred_file = 'meal/management/commands/credential/new_user_credentials.csv'
        aws_access_key_id = ''
        aws_secret_access_key = ''
        with open(aws_cred_file) as acf:
           ac_dataset = csv.reader(acf)
           for ac_data in ac_dataset:
               if ac_data[0] == 'pbf':
                   aws_access_key_id = ac_data[2]
                   aws_secret_access_key = ac_data[3]

        for meal_data in meal_dataset:
            # extract data
            uuid = meal_data.uuid
            text = meal_data.comment

            # initialize sentiment parameter
            positive = 0.0
            negative = 0.0
            neutral = 0.0
            mixed = 0.0

            # request to aws comprehend
            if text:
                result = self.detect_sentiment(
                    text, aws_access_key_id, aws_secret_access_key, language_code)
                result_object = json.loads(json.dumps(result))
                positive = result_object['SentimentScore']['Positive']
                negative = result_object['SentimentScore']['Negative']
                neutral = result_object['SentimentScore']['Neutral']
                mixed = result_object['SentimentScore']['Mixed']
                
            # save aws sentiment analysis result
            aws_sa = AwsSentimentAnalysis.objects.create(
                positive=positive,
                negative=negative,
                neutral=neutral,
                mixed=mixed
            )

            # link aws sentiment analysis result to meal menu
            meal_menu = MealMenu.objects.get(uuid=uuid)
            meal_menu.aws_sa = aws_sa
            meal_menu.save()
