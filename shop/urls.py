from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("tracker/", views.tracker, name="Tracker"),
    path("search/", views.search, name="Search"),
    path("productView/<int:myid>", views.productView, name="ProductView"),
    path("checkout/", views.checkout, name="Checkout"),
    path("register/", views.register, name="Register"),
    path("login/", views.login, name="Login"),
    path("logout/", views.logout, name="Logout"),
    path("handlerequest/", views.handlerequest, name="HandleRequest"),
    path("demopayment/", views.demopayment, name="DemoPayment"),
    path("thankyou/", views.thankyou, name="ThankYou"),

]
