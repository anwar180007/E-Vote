from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
user_gender = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others'),
)
class Voter_Registration(User):
    father_name = models.CharField(max_length= 150)
    mother_name = models.CharField(max_length= 150)
    gender = models.CharField(max_length=200, choices= user_gender)
    dob = models.DateTimeField()
    village = models.CharField(max_length= 150)
    post_office = models.CharField(max_length= 150)
    upazilla = models.CharField(max_length= 150)
    zilla = models.CharField(max_length= 150)
    profile_pic = models.ImageField(upload_to="myimage")

    def __str__(self):
        return str(self.username)

nominate_position =(
    ('Chairman', 'Chairman'),
    ('Member', 'Member'),
)
class Nomination_list(models.Model):
    candidate_name = models.CharField(max_length= 200)
    icon_name = models.CharField(max_length=100, default="....")
    ballot_paper_img = models.ImageField(upload_to="myimage")
    position = models.CharField(
        max_length=50,
        choices= nominate_position,
        default= '...',
    )

class Nomination_paper(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(
        max_length=50,
        choices= nominate_position,
        default= 'Member',
    )
    paper_img = models.ImageField(upload_to = "myimage")


class Vote_Shedule(models.Model):
    # year = models.CharField(max_length=10)
    vote_date = models.DateTimeField()

class Chairman_Vote_Data(models.Model):
    voter_id = models.CharField(max_length= 200, default='...')
    voter_name = models.CharField(max_length= 200)
    candidate_name = models.CharField(max_length= 200)
    icon_name = models.CharField(max_length=100, default="....")
    ballot_paper_img = models.ImageField(upload_to="myimage")

class Member_Vote_Data(models.Model):
    voter_id = models.CharField(max_length= 200, default='...')
    voter_name = models.CharField(max_length= 200)
    candidate_name = models.CharField(max_length= 200)
    icon_name = models.CharField(max_length=100, default="....")
    ballot_paper_img = models.ImageField(upload_to="myimage")