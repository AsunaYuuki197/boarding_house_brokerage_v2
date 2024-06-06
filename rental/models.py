from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# class User(AbstractUser):
#     pass

class House(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    description = models.TextField()
    reputation_score = models.FloatField(default=0.0)
    price = models.DecimalField(max_digits=10, decimal_places=0, default=3000000)

    def __str__(self):
        return self.name

class HouseImage(models.Model):
    house = models.ForeignKey(House, related_name='image', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='house_images/')

class RentalPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)
    total_vacancies = models.PositiveIntegerField(default=1)
    available_vacancies = models.PositiveIntegerField(default=1)
    def __str__(self):
        return self.title

class Verification(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]
    rental_post = models.ForeignKey(RentalPost, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    comments = models.TextField(blank=True)

    def __str__(self):
        return f"{self.rental_post.title} - {self.status}"

class Review(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class ReviewReply(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Reservation(models.Model):
    REFUND_STATUS_CHOICES = [
        ('none', 'No Refund'),
        ('requested', 'Refund Requested'),
        ('processed', 'Refund Processed')
    ]    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rental_post = models.ForeignKey(RentalPost, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_paid = models.BooleanField(default=False)
    refund_status = models.CharField(max_length=10, choices=REFUND_STATUS_CHOICES, default='none')

class Payment(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)

