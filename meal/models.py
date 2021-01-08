from django.db import models
import uuid

# Create your models here.
class MealType(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    meal_type = models.CharField(max_length=16, null=True)

    def __str__(self):
        return self.meal_type

class AwsSentimentAnalysis(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    neutral = models.FloatField(default=0.0)
    positive = models.FloatField(default=0.0)
    negative = models.FloatField(default=0.0)
    mixed = models.FloatField(default=0.0)

class AzureSentimentAnalysis(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    neutral = models.FloatField(default=0.0)
    positive = models.FloatField(default=0.0)
    negative = models.FloatField(default=0.0)
    mixed = models.FloatField(default=0.0)

class GcpSentimentAnalysis(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    magnitude = models.FloatField(default=0.0)
    score = models.FloatField(default=0.0)

class MealMenu(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(null=True)
    menu = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    meal_type = models.ForeignKey(MealType, on_delete=models.CASCADE, null=True)
    aws_sa = models.ForeignKey(AwsSentimentAnalysis, on_delete=models.CASCADE, null=True)
    azure_sa = models.ForeignKey(AzureSentimentAnalysis, on_delete=models.CASCADE, null=True)
    gcp_sa = models.ForeignKey(GcpSentimentAnalysis, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.menu
