from django.db import models

class MovieCityProcess(models.Model):
    movie = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    process_id = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.movie} - {self.city}"

class MovieCityPhoneNumber(models.Model):
    movie = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15) 

    def __str__(self):
        return f"{self.movie} - {self.city} - {self.phone_number}"
