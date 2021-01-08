# -*- coding: utf-8 -*-
import csv
import datetime
from django.core.management.base import BaseCommand, CommandError
from meal.models import MealType, MealMenu

class Command(BaseCommand):

    def handle(self, *args, **options):

        meal_menus = MealMenu.objects.all()

        mm_gcp_sa_arrays = []

        for meal_menu in meal_menus:
            mm_gcp_sa_array = [
                meal_menu.date,
                meal_menu.meal_type.meal_type,
                meal_menu.menu,
                meal_menu.comment,
                meal_menu.gcp_sa.magnitude,
                meal_menu.gcp_sa.score,
                meal_menu.gcp_sa.magnitude * meal_menu.gcp_sa.score,
            ]
            mm_gcp_sa_arrays.append(mm_gcp_sa_array)
        
        print(mm_gcp_sa_arrays)

        # csv file
        mm_gcp_sa_file = 'meal/results_gcp_sa.csv'

        with open(mm_gcp_sa_file, 'w') as results_file:
            writer = csv.writer(results_file)
            writer.writerows(mm_gcp_sa_arrays)
