from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_("email address"), blank=True, unique=True)
    image = models.ImageField('Image', upload_to='user_images/')
    phone = models.CharField('Phone number', max_length=15)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    @property
    def profile_picture(self):
        if self.image:
            return self.image

    def __str__(self):
        return self.email
    
    class Meta:
        swappable = 'AUTH_USER_MODEL'