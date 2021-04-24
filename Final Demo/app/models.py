from django.contrib.auth.models import User
from django.db import models


#user profile model
from django.db.models.signals import post_save
from django.dispatch import receiver


class State(models.Model):
    name = models.CharField(max_length=400)
    abbr = models.CharField(max_length=2)

    def __str__(self):
        return self.name


class Profile(models.Model):
    US_STATES = (('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'),
                 ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'),
                 ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'),
                 ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'),
                 ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'),
                 ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'),
                 ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'),
                 ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'),
                 ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'),
                 ('NY', 'New York'),
                 ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'),
                 ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'),
                 ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'),
                 ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'),
                 ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming'))

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_Name = models.CharField(max_length=50, default='', blank=False)
    address_1 = models.CharField(max_length=100, default='', blank=False)
    address_2 = models.CharField(max_length=100, default='', blank=True)
    city = models.CharField(max_length=100, default='', blank=False)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=False)
    zipcode = models.CharField(max_length=9, blank=False, default='')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance=None, created=None, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class FuelQuote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gallons_requested = models.DecimalField(max_digits=10000, decimal_places=2, default=0.00)
    delivery_date = models.DateField()
    delivery_address = models.CharField(max_length=200)
    rate = models.DecimalField('Price/Gallon', decimal_places=4, max_digits=10000, default=1.50)

    def get_total(self):
        return self.gallons_requested * self.rate

    def __str__(self):
        return self.user.username
