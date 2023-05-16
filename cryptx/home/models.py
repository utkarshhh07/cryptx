from django.db import models

# Create your models here.

class Forgotpassword(models.Model):
    email = models.EmailField(max_length=100)
    token = models.CharField(max_length=500)
    datastamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email