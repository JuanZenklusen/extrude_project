from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Ampliación del modelo de usuario mediante un enlace uno a uno
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    cod_phone = models.CharField(max_length=5, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    day = models.IntegerField(null=True, blank=True,)
    month = models.IntegerField(null=True, blank=True,)
    year = models.IntegerField(null=True, blank=True,)

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 300 or img.width > 300:
            new_img = (300, 300)
            img.thumbnail(new_img)
            img.save(self.avatar.path)


class Contact(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    phone = models.CharField(max_length=18, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    subject = models.CharField(max_length=150, blank=False, null=False)
    consult = models.CharField(max_length=500, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.subject} - {self.consult}'