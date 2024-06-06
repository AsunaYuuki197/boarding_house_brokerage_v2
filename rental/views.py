from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.contrib import messages
from django.db.models import Avg

from .forms import *
from .models import *

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def home(request):
    rental_posts = RentalPost.objects.filter(is_verified=True)
    houses = []
    for rental_post in rental_posts:
        houses.append((rental_post.house, HouseImage.objects.filter(house=rental_post.house).first()))

    return render(request, 'home.html', {'houses': houses})


def house_detail(request, pk):
    house = get_object_or_404(House, pk=pk)
    reviews = Review.objects.filter(house=house)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    images = HouseImage.objects.filter(house=house)
    posts = RentalPost.objects.filter(house=house)

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.house = house
            review.user = request.user
            review.save()
            reviews = Review.objects.filter(house=house)
            average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
            house.reputation_score = average_rating
            house.save()
            return redirect('house_detail', pk=house.pk)
    else:
        review_form = ReviewForm()
    
    return render(request, 'house_detail.html', {
        'house': house,
        'post': posts[0],
        'reviews': reviews,
        'average_rating': average_rating,
        'images': images,
        'review_form': review_form
    })



@login_required
def create_rental_post(request):
    if request.method == 'POST':
        house_form = HouseForm(request.POST)
        rental_post_form = RentalPostForm(request.POST)
        images = request.FILES.getlist('images')
        if house_form.is_valid() and rental_post_form.is_valid():
            house = house_form.save()
            rental_post = rental_post_form.save(commit=False)
            rental_post.user = request.user
            rental_post.house = house
            rental_post.save()
            for image in images:
                HouseImage.objects.create(house=house, image=image)
            return redirect('home')
    else:
        house_form = HouseForm(request.POST)
        rental_post_form = RentalPostForm(request.POST)

    return render(request, 'create_rental_post.html', {
        'house_form': house_form,
        'rental_post_form': rental_post_form      
    })


@staff_member_required
def manage_posts(request):
    posts = RentalPost.objects.all()
    return render(request, 'manage_posts.html', {'posts': posts})

@staff_member_required
def manage_reviews(request):
    reviews = Review.objects.all()
    return render(request, 'manage_reviews.html', {'reviews': reviews})

@login_required
def manage_user_posts(request):
    posts = RentalPost.objects.filter(user=request.user)
    return render(request, 'manage_user_posts.html', {'posts': posts})

@login_required
def manage_user_reviews(request):
    reviews = Review.objects.filter(user=request.user)
    return render(request, 'manage_user_reviews.html', {'reviews': reviews})

@staff_member_required
def verify_post(request, pk):
    rental_post = get_object_or_404(RentalPost, pk=pk)
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            verification = form.save(commit=False)
            verification.rental_post = rental_post
            verification.save()
            rental_post.is_verified = True if verification.status == 'approved' else False
            rental_post.save()
            return redirect('manage_posts')
    else:
        form = VerificationForm()
    return render(request, 'verify_post.html', {'form': form, 'rental_post': rental_post})

@staff_member_required
def delete_post(request, pk):
    post = get_object_or_404(RentalPost, pk=pk)
    post.house.delete()
    return redirect('manage_posts')

@staff_member_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    review.delete()
    return redirect('manage_reviews')


@login_required
def reply_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        form = ReviewReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.review = review
            reply.user = request.user
            reply.save()
            return redirect('house_detail', pk=review.house.pk)
    else:
        form = ReviewReplyForm()
    return render(request, 'reply_review.html', {'form': form, 'review': review})


def customer_care(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            send_mail(
                f"Customer Care Inquiry from {form.cleaned_data['name']}",
                form.cleaned_data['message'],
                form.cleaned_data['email'],
                ['support@boardinghouse.com']
            )
            return redirect('home')
    else:
        form = ContactForm()
    return render(request, 'customer_care.html', {'form': form})
    

@login_required
def reserve_house(request, pk):
    rental_post = get_object_or_404(RentalPost, pk=pk)
    if rental_post.available_vacancies <= 0:
        return redirect('house_detail', pk=pk)
    
    if request.method == 'POST':
        reservation_form = ReservationForm(request.POST)
        if reservation_form.is_valid():
            reservation = reservation_form.save(commit=False)
            reservation.user = request.user
            reservation.rental_post = rental_post
            reservation.save()
            rental_post.available_vacancies -= 1
            rental_post.save()
            return redirect('payment', pk=reservation.pk)
    else:
        reservation_form = ReservationForm()
    return render(request, 'reserve_house.html', {'reservation_form': reservation_form, 'rental_post': rental_post})

@login_required
def payment(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    house_price = reservation.rental_post.house.price
    service_fee = float(house_price) * 0.02
    total_amount = float(house_price) + service_fee

    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            payment = payment_form.save(commit=False)
            payment.reservation = reservation
            payment.amount = total_amount
            payment.save()
            reservation.is_paid = True
            reservation.save()
            return redirect('home')
    else:
        payment_form = PaymentForm()
    return render(request, 'payment.html', {
        'payment_form': payment_form,
        'reservation': reservation,
        'house_price': house_price,
        'service_fee': service_fee,
        'total_amount': total_amount
    })


@login_required
@staff_member_required
def manage_reservations(request):
    reservations = Reservation.objects.all()
    return render(request, 'manage_reservations.html', {'reservations': reservations})

@login_required
def manage_user_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'manage_user_reservations.html', {'reservations': reservations})

@login_required
def manage_user_rental_reservations(request):
    reservations = Reservation.objects.filter(rental_post__user=request.user)
    return render(request, 'manage_user_rental_reservations.html', {'reservations': reservations})

@login_required
def refund_request(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        form = RefundRequestForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('manage_user_reservations')
    else:
        form = RefundRequestForm(instance=reservation)
    return render(request, 'refund_request.html', {'form': form, 'reservation': reservation})

@login_required
def manage_user_rental_reservations(request):
    reservations = Reservation.objects.filter(rental_post__user=request.user)
    return render(request, 'manage_user_rental_reservations.html', {'reservations': reservations})

@login_required
def refund_request(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        form = RefundRequestForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Refund request submitted.')
            return redirect('manage_user_reservations')
    else:
        form = RefundRequestForm(instance=reservation)
    return render(request, 'refund_request.html', {'form': form, 'reservation': reservation})

@login_required
@staff_member_required
def process_refund(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    reservation.refund_status = 'processed'
    reservation.rental_post.available_vacancies += 1
    reservation.rental_post.save()
    reservation.save()
    messages.success(request, 'Refund processed successfully.')
    return redirect('manage_reservations')

@login_required
@staff_member_required
def delete_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    reservation.rental_post.available_vacancies += 1
    reservation.rental_post.save()
    reservation.delete()
    messages.success(request, 'Reservation aborted successfully.')
    return redirect('manage_reservations')

@login_required
def user_delete_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if reservation.rental_post.user == request.user or reservation.user == request.user:
        reservation.rental_post.available_vacancies += 1
        reservation.rental_post.save()
        reservation.delete()
        messages.success(request, 'Reservation aborted successfully.')
        return redirect('manage_user_rental_reservations')
    return redirect('home')