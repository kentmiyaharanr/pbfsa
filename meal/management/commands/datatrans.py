# -*- coding: utf-8 -*-
import csv
import datetime
from django.core.management.base import BaseCommand, CommandError
from meal.models import MealType, MealMenu

class Command(BaseCommand):

    def handle(self, *args, **options):
        # create meal type
        meal_types = ['breakfast', 'lunch', 'dinner']
        for meal_type in meal_types:
            MealType.objects.create(meal_type=meal_type)

        # uuids
        uuid_breakfast = MealType.objects.get(meal_type=meal_types[0]).uuid
        uuid_lunch = MealType.objects.get(meal_type=meal_types[1]).uuid
        uuid_dinner = MealType.objects.get(meal_type=meal_types[2]).uuid

        # # csv files
        csv_dir = 'meal/management/commands/csv/'
        file_breakfast = csv_dir + 'pbf_meal_mgmt_breakfast.csv'
        file_lunch = csv_dir + 'pbf_meal_mgmt_lunch.csv'
        file_dinner = csv_dir + 'pbf_meal_mgmt_dinner.csv'

        # datasets
        meal_dataset = [
            [uuid_breakfast, file_breakfast],
            [uuid_lunch, file_lunch],
            [uuid_dinner, file_dinner]
        ]

        # Load csv dataset to database
        for meal_data in meal_dataset:
            # uuid and filename
            uuid_meal = meal_data[0]
            file_meal = meal_data[1]

            # meal type object
            mtype = MealType.objects.get(uuid=uuid_meal)

            # read csv and write data to database
            with open(file_meal) as fm:
                mdataset = csv.reader(fm)
                for mdata in mdataset:
                    if mdata[0] != 'date':
                        MealMenu.objects.create(
                            date=datetime.datetime.strptime(mdata[0], '%Y/%m/%d'),
                            menu=mdata[1],
                            comment=mdata[2],
                            meal_type=mtype
                        )
