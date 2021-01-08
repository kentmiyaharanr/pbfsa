from django.contrib import admin
from .models import MealType, AwsSentimentAnalysis, AzureSentimentAnalysis, GcpSentimentAnalysis, MealMenu

# Register your models here.
admin.site.register(MealType)
admin.site.register(AwsSentimentAnalysis)
admin.site.register(AzureSentimentAnalysis)
admin.site.register(GcpSentimentAnalysis)
admin.site.register(MealMenu)
