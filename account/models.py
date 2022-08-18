from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from PIL import Image

favorites_list = (
    ('백엔드', '백엔드'),
    ('프론트엔드', '프론트엔드'),
    ('Andriod','Andriod'),
    ('iOS','iOS')
)


class UserManager(BaseUserManager):
    def create_user(self, email, name,date_of_birth, favorites_1, favorites_2 , password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            favorites_1 = favorites_1,
            favorites_2 = favorites_2,
            name = name,
        )



        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, favorites_1, favorites_2, password,name):
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
            favorites_1 =favorites_1,
            favorites_2 = favorites_2,
            name = name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    favorites_1 = models.CharField(max_length= 200, choices = favorites_list, default='')
    favorites_2 = models.CharField(max_length= 200, choices = favorites_list, default='')
    name = models.CharField(max_length= 200, default='')
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')

    
    def __str__(self):
        return self.user.email



    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth','favorites_1','favorites_2','name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     image = models.ImageField(blank=True)                

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='media/button.png', upload_to='media/')

    def __str__(self):
        return self.user.email

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        new_img = (132, 132)
        img.thumbnail(new_img)
        img.save(self.avatar.path)
