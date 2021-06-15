from django.db import models
from django.contrib.auth.models import User
from django.core.validators import *
from django.conf import settings
from fontawesome.fields import IconField
# Create your models here.
class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    name = models.CharField(max_length=20, blank=False, null=False,
                            validators=[MinLengthValidator(2, message='Name should atleast have 2 characters')
                                        ])

    email = models.EmailField(blank=False, null=False, default='ex@ex.com')

    image = models.ImageField(null=True,blank=True, upload_to='images/')


    def __str__(self):
        return self.user.username

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = 'images/placeholder.png'
        print(url)
        return url



class Tutor(models.Model):
    userInfo = models.OneToOneField(UserInfo, on_delete=models.CASCADE, blank=True)

    bio = models.TextField(max_length=80, blank=True, null= True)

    about = models.TextField(max_length=300, blank=False, null=False)

    phone = models.IntegerField(blank=True,null=True)

    dob = models.DateField(blank=False, null=False)

    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_DoNotSpecify = 2
    GENDER_CHOICES = [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female'), (GENDER_DoNotSpecify, 'Do Not Specify')]
    gender = models.IntegerField(choices=GENDER_CHOICES)

    subjects = models.CharField(max_length= 50, blank=False, null=False,
                                validators=[MinLengthValidator(2, message='Length should atleast have 2 characters')],
                                help_text='Subject 1, Subject 2, Subject 3...')

    cv = models.FileField(blank=False, upload_to='cv/',validators=[FileExtensionValidator(allowed_extensions=['pdf'], message='Please choose a .pdf file.')])


    twitter_link = models.URLField(max_length=250, blank=True, null=True)
    facebook_link = models.URLField(max_length=250, blank=True, null=True)
    instagram_link = models.URLField(max_length=250, blank=True, null=True)
    github_link = models.URLField(max_length=250, blank=True, null=True)
    linkedin_link = models.URLField(max_length=250, blank=True, null=True)
    youtube_link = models.URLField(max_length=250, blank=True, null=True)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return ('Tutor: '+ self.userInfo.name)



    @property
    def cvURL(self):
        return self.cv.url

class Client(models.Model):
    userInfo = models.OneToOneField(UserInfo, on_delete=models.CASCADE, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return ('Client: '+ self.userInfo.name)


class Comment(models.Model):
    text = models.TextField(validators=[MinLengthValidator(2, message='Comment should atleast have 2 characters')
    ])

    owner = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

class Favourite(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('tutor', 'user', 'id')

    def __str__(self):
        return '%s likes %s -- %d' % (self.user.username, self.tutor.userInfo.name, self.id)







