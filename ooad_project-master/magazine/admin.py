from django.contrib import admin
from .models import CategoriesList,Books,OrdersPayment,PaymentProblem
# Register your models here.
class CategoriesListRef(admin.ModelAdmin):
    list_display = ['category_name']
admin.site.register(CategoriesList,CategoriesListRef)
class BooksRef(admin.ModelAdmin):
    list_display = ['id','name','author','description','categorylist','subscription_cost','book_image']
admin.site.register(Books,BooksRef)
class OrdersPaymentRef(admin.ModelAdmin):
    list_display = ['order_id','amount','username','user_email','payment_for','status','created_at','updated_at']
admin.site.register(OrdersPayment,OrdersPaymentRef)
class paymentProblemRef(admin.ModelAdmin):
    list_display = ['amount','username','user_email','payment_for','description','created_at','updated_at']
admin.site.register(PaymentProblem,paymentProblemRef)