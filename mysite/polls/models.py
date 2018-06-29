from django.db import models
import datetime
from django.utils import timezone

class Question(models.Model):
    question_text=models.CharField(max_length=200)
    pub_date=models.DateTimeField("date publised")
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now=timezone.now()
        return now-datetime.timedelta(days=1)<=self.pub_date<=now
    was_published_recently.admin_order_fields="pub_date"
    was_published_recently.boolean=True
    was_published_recently.short_description="Published recently?"


class Choice(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    choice_text=models.CharField(max_length=200)
    votes=models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

class CurrencyRate(models.Model):
    RateID=models.BigAutoField(primary_key=True)
    SourceCode=models.CharField(max_length=50)
    CurrencyCode=models.CharField(max_length=3)
    SellPrice=models.DecimalField(max_digits=15,decimal_places=6)
    BuyPrice=models.DecimalField(max_digits=15,decimal_places=6)
    CreateTime=models.DateTimeField(auto_now=True)