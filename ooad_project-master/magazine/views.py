from django.shortcuts import render
from django.http import HttpResponse
from .models import CategoriesList,Books,PaymentProblem,OrdersPayment
import razorpay
import time
from decouple import config
from django.views.decorators.csrf import csrf_exempt


keyid = config('KEYID')
keySecret = config('KEYSECRET')
client = razorpay.Client(auth=(keyid, keySecret))

def home(request):
     categories = CategoriesList.objects.all()
     books = Books.objects.all()
     #print(categories)
     return render(request, 'home.html',{'categories':categories,'books':books})

def payment(request,id):
     book = Books.objects.get(id=id)
     print(book.subscription_cost)
     data = {
     'amount' : int(book.subscription_cost)*100,
     'currency' : "INR",
     'receipt' : f"Krishna-{int(time.time())}",
     'notes' : {
          'name' : request.user.username,
          'payment_for' : book.name,
          }
     }
     try:
          order = client.order.create(data=data)
          order_id = order['id']
          status = "pending"
          OrdersPayment.objects.create(order_id=order_id,amount=book.subscription_cost,username=request.user.username,user_email=request.user.email,payment_for=book.name,status=status)
          return render(request,'payment.html',{'order': order,'book':book})
     except Exception as e:
          print(e)
          PaymentProblem.objects.create(amount=book.subscription_cost,username=request.user.username,user_email=request.user.email,payment_for=book.name,description=e)
          return render(request,'payment.html',{'description': e})
     return HttpResponse("Not a valid page. <a href='/dashboard'>Click here</a> to redirect to home page")

@csrf_exempt
def success(request):
     if request.method == "POST":
          data = request.POST
          # razorpay_order_id = ""
          # razorpay_payment_id = ""
          razorpay_order_id = data["razorpay_order_id"]
          razorpay_payment_id = data["razorpay_payment_id"]
          payment_razorpay = client.payment.fetch(razorpay_payment_id)
          trusted_order = OrdersPayment.objects.filter(order_id=razorpay_order_id)
          if trusted_order:
               try:
                    client.utility.verify_payment_signature(data)
                    trusted_order.update(payment_id = razorpay_payment_id, status = "Success")
                    payment_details = OrdersPayment.objects.get(order_id = razorpay_order_id)
                    return render(request,'success.html',{'payment_details': payment_details})
               except Exception as e:
                    trusted_order.update(payment_id = razorpay_payment_id, status = "Failed")
                    payment_details = OrdersPayment.objects.get(order_id = razorpay_order_id)
                    print(e)
                    return render(request,'success.html',{'payment_details': payment_details})
     else:
          trusted_order.update(payment_id = razorpay_payment_id,  status = "Suspicious")
          payment_details = OrdersPayment.objects.get(order_id = razorpay_order_id)
          return render(request,'success.html',{'payment_details': payment_details})
     return HttpResponse("Not a valid page. <a href='/app'>Click here</a> to redirect to home page")