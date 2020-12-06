


from django.db import models
from .tasks import elk_insertion_single_registry

# Create your models here.

class MeasurementsManager(models.Manager):
    def get_by_natural_key(self, date,PJME_MW):
        return self.get(date=date, PJME_MW=PJME_MW)

class Measurements(models.Model):
    objects = MeasurementsManager() 

    id=models.AutoField(primary_key=True)
    date  = models.DateTimeField(null=False, unique=True)
    PJME_MW = models.FloatField(default=0, null=False) 

    def natural_key(self):
        return (self.date, self.PJME_MW)

    def save (self, *args, **kwargs):
        super().save(*args, **kwargs)
        print(self.date, self.PJME_MW)
        elk_insertion_single_registry.delay(self.id)           

    
class ForecastModels(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(default='fbprophet', max_length=50, null=False)
    train_initial_date = models.DateTimeField(null=False)
    train_last_date = models.DateTimeField(null=False)
    test_score = models.FloatField(null=False, default=0)
    test_accuracy = models.FloatField(null=False, default=0)
    status = models.BooleanField(null=False, default=True)

    class Meta:
        unique_together = ('name', 'train_initial_date','train_last_date')


class Forecasts(models.Model):
    id=models.AutoField(primary_key=True)
    PJME_MW = models.FloatField(default=0)
    date = models.DateTimeField(null=False)
    error = models.FloatField(default=0)
    percentage_error = models.FloatField(default=0)

    forecast_model = models.ForeignKey(ForecastModels, to_field='id', on_delete=models.CASCADE)
    measurement = models.ForeignKey(Measurements, null=True, to_field='id',on_delete=models.CASCADE)

