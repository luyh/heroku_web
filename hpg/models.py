from django.db import models

# Create your models here.
class hpg_model(models.Model):
    keyword = models.CharField(max_length=30)
    main_link = models.IntegerField()
    image = models.ImageField()

    def __str__(self):
        return self.name