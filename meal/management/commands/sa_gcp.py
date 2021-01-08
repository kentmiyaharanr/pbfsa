# -*- coding: utf-8 -*-
import os
import csv
import datetime
import json
from google.cloud import language_v1
from django.core.management.base import BaseCommand, CommandError
from meal.models import MealType, MealMenu, GcpSentimentAnalysis

class Command(BaseCommand):

    def handle(self, *args, **options):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS']='meal/management/commands/credential/heroic-ruler-300921-0c496dea9447.json'

        # Meal dataset 
        meal_dataset = MealMenu.objects.all()

        for meal_data in meal_dataset:
            # extract data
            uuid = meal_data.uuid
            text = meal_data.comment

            # initialize sentiment parameter
            score = 0.0
            magnitude = 0.0

            # request to gcp natural language
            if text:
                # Instantiates a client
                client = language_v1.LanguageServiceClient()

                document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

                # Detects the sentiment of the text
                sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

                score = sentiment.score
                magnitude = sentiment.magnitude

            # save gcp sentiment analysis result
            gcp_sa = GcpSentimentAnalysis.objects.create(
                magnitude=magnitude,
                score=score
            )

            # link gcp sentiment analysis result to meal menu
            meal_menu = MealMenu.objects.get(uuid=uuid)
            meal_menu.gcp_sa = gcp_sa
            meal_menu.save()
