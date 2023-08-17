import stripe
import json
from django.shortcuts import render
from django.template import loader

from .models import StudentContact, Event, Product, ProductSale, ServicesSale, ContactUs, ProductTransaction, \
    ServiceTransaction, Yelp, Announcement
from django.http import HttpResponse
from django.conf import settings
from django.http.response import JsonResponse  # new
from django.views.decorators.csrf import csrf_exempt

import smtplib
from email.message import EmailMessage


def send_email(to, subject, message):
    try:
        email_address = settings.SEND_EMAIL_HOST
        email_password = settings.SEND_EMAIL_PASSWORD

        if email_address is None or email_password is None:
            # no email address or password
            # something is not configured properly
            return False

        # create email
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = email_address
        msg['To'] = to
        msg.set_content(message)

        # send email
        with smtplib.SMTP_SSL('mail.greatknightschess.com', 465) as smtp:
            smtp.login(email_address, email_password)
            smtp.send_message(msg)
        return True
    except Exception as e:
        return JsonResponse({'error': str(e)})
    return False


confirmation_message = """

Dear Sir,

We wanted to inform you that we have received your payment for the service you signed up for on our website.
 
Thank you for choosing greatknightschess.com!

Best regards,

Great Knight Chess
"""


def message_for_service(coach, std_name, instructor, school, session, duration, price, email, phone):
    seller_confirmation_message_for_service = """

Dear {},

We are pleased to inform you that payment has been received for the service placed on your website with following details:

Student Name:{}
Instructor:{}
School:{}
Session:{}
Duration:{}
Price:${}
Email:{}
Phone:{}

Best regards,

Great Knight Chess
""".format(coach, std_name, instructor, school, session, duration, price, email, phone)

    return seller_confirmation_message_for_service


def message_for_product(coach, firstname, lastname, product, quantity, total, email, phone):
    seller_confirmation_message_for_service = """

Dear {},

We are pleased to inform you that payment has been received for an order placed on your website with following details:

First Name:{}
Last Name:{}
Product:{}
Quantity:{}
Total:${}
Email:{}
Phone:{}

Best regards,

Great Knight Chess
""".format(coach, firstname, lastname, product, quantity, total, email, phone)

    return seller_confirmation_message_for_service


seller_confirmation_message_for_product = """

Dear Service Provider,

We are pleased to inform you that payment has been received for the order placed on your website.

Thank you for your prompt and efficient service!

Best regards,

Great Knight Chess
"""


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


def create_checkout_session(request):
    if request.method == 'POST':
        domain_url = 'https://greatknightschess.com/payment'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        transaction = ProductTransaction.objects.create(
            payment_status="INITIATED",
        )
        try:
            mydata = json.loads(request.body)
            order_total = 0
            for order_item in mydata['productsData']:
                order_total = order_total + (int(order_item['price']) * int(order_item['quantity']))
            line_items = []
            for order_item in mydata['productsData']:
                product_data = dict()
                line_item = dict()
                price_data = dict()
                price_data["unit_amount"] = int(order_item['price']) * 100
                price_data["currency"] = "usd"
                product_data["name"] = order_item['name']
                product_data["images"] = [
                    f"{settings.SITE_URL}/media/{order_item['image']}"
                ]
                price_data["product_data"] = product_data
                line_item["price_data"] = price_data
                line_item["quantity"] = order_item['quantity']
                line_items.append(line_item)
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + '?q=success',
                cancel_url=domain_url + '?q=cancelled',
                payment_method_types=['card'],
                mode='payment',
                metadata={
                    'transaction_id': transaction.id,
                    'type': 'product',
                },
                payment_intent_data={
                    "metadata": {
                        'transaction_id': transaction.id,
                        'type': 'product',
                    }
                },
                line_items=line_items,
            )
            for order_item in mydata['productsData']:
                form = ProductSale(
                    email=mydata['customerInformation']['email'],
                    phone_number=mydata['customerInformation']['phone'],
                    first_name=mydata['customerInformation']['First_Name'],
                    last_name=mydata['customerInformation']['Last_Name'],
                    country=mydata['customerInformation']['country'],
                    street=mydata['customerInformation']['Street_Address'],
                    apt=mydata['customerInformation']['Apt'],
                    postal_code=mydata['customerInformation']['Postal'],
                    city=mydata['customerInformation']['city'],
                    total=int(order_item['quantity']) * int(order_item['price']),
                    product=Product.objects.get(id=order_item['id']),
                    quantity=order_item['quantity'],
                    transaction=transaction
                )
                product = Product.objects.get(id=order_item['id'])
                product.quantity = product.quantity - int(order_item['quantity'])
                product.save()
                form.save()
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@csrf_exempt
def stripe_webhook_view(request):
    event = None
    payload = request.body
    sig_header = request.headers['STRIPE_SIGNATURE']
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEB_HOOK_KEY
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e
    if event['type'] == 'payment_intent.payment_failed':
        transaction_id = int(event['data']['object']['metadata']['transaction_id'])
        transaction_type = event['data']['object']['metadata']['type']
        if transaction_type == 'service':
            transaction_object = ServiceTransaction.objects.get(id=transaction_id)
        else:
            transaction_object = ProductTransaction.objects.get(id=transaction_id)
        transaction_object.payment_status = "FAILED"
        transaction_object.save()
    elif event['type'] == 'payment_intent.succeeded':
        transaction_id = int(event['data']['object']['metadata']['transaction_id'])
        transaction_type = event['data']['object']['metadata']['type']
        if transaction_type == 'service':
            transaction_object = ServiceTransaction.objects.get(id=transaction_id)
            sale = ServicesSale.objects.get(transaction=transaction_id)
            message1 = message_for_service("Seth", sale.st_first_name, sale.event.instructor_name,
                                           sale.event.school_name, sale.event.session, sale.event.duration,
                                           sale.event.price, sale.email, sale.phone_number_one)
            message2 = message_for_service("Shaun", sale.st_first_name, sale.event.instructor_name,
                                           sale.event.school_name, sale.event.session, sale.event.duration,
                                           sale.event.price, sale.email, sale.phone_number_one)
            send_email(sale.email, "Payment Received - Welcome to Great Knight Chess!", confirmation_message)
            send_email("coachseth@greatknightschess.com", "Payment Received", message1)
            send_email("shaunlowney@greatknightschess.com", "Payment Received", message2)
        else:
            transaction_object = ProductTransaction.objects.get(id=transaction_id)
            sale = ProductSale.objects.get(transaction=transaction_id)
            message1 = message_for_product("Seth", sale.first_name, sale.last_name, sale.product.product_name,
                                           sale.quantity, sale.total, sale.email, sale.phone_number)
            message2 = message_for_product("Shaun", sale.first_name, sale.last_name, sale.product.product_name,
                                           sale.quantity, sale.total, sale.email, sale.phone_number)
            send_email(sale.email, "Payment Received - Welcome to Great Knight Chess!", confirmation_message)
            send_email("coachseth@greatknightschess.com", "Payment Received", message1)
            send_email("shaunlowney@greatknightschess.com", "Payment Received", message2)
        transaction_object.payment_status = "SUCCEEDED"
        transaction_object.save()
    return HttpResponse(status=200)


def _handle_successful_payment(checkout_session):
    # Define what to do after the user has successfully paid
    pass


def services_checkout_session(request):
    if request.method == 'POST':
        mydata = json.loads(request.body)
        domain_url = 'https://greatknightschess.com/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        transaction = ServiceTransaction.objects.create(
            payment_status="INITIATED",
        )
        try:
            order_total = 0
            for order_item in mydata['productsData']:
                order_total = order_total + int(order_item['price'])
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + '?q=success',
                cancel_url=domain_url + '?q=cancelled',
                payment_method_types=['card'],
                mode='payment',
                metadata={
                    'transaction_id': transaction.id,
                    'type': 'service',
                },
                payment_intent_data={
                    "metadata": {
                        'transaction_id': transaction.id,
                        'type': 'service',
                    }
                },
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': order_total * 100,
                        'product_data': {
                            'name': 'Services',
                        },
                    },
                    'quantity': 1,
                }],
            )

            for order_item in mydata['productsData']:
                form = ServicesSale(
                    st_first_name=mydata['customerInformation']['st_first_name'],
                    st_last_name=mydata['customerInformation']['st_last_name'],
                    grade_level=mydata['customerInformation']['grade_level'],
                    pr_first_name=mydata['customerInformation']['pr_first_name'],
                    pr_last_name=mydata['customerInformation']['pr_last_name'],
                    phone_number_one=mydata['customerInformation']['phone_number_one'],
                    phone_number_two=mydata['customerInformation']['phone_number_two'],
                    email=mydata['customerInformation']['email'],
                    emr_first_name=mydata['customerInformation']['emr_first_name'],
                    emr_last_name=mydata['customerInformation']['emr_last_name'],
                    emr_phone_number=mydata['customerInformation']['emr_phone_number'],
                    relation=mydata['customerInformation']['relation'],
                    amount_paid=order_item['price'],
                    transaction=transaction,
                    event=Event.objects.get(id=order_item['id'])
                )
                form.save()
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


def get_name(request):
    if request.method == 'POST':
        school_name = request.POST.get('school_name')
        student_first_name = request.POST.get('student_first_name')
        student_last_name = request.POST.get('student_last_name')
        grade_level = request.POST.get('grade_level')
        parents_first_name = request.POST.get('parents_first_name')
        parents_last_name = request.POST.get('parents_last_name')
        parent_phone_one = request.POST.get('parent_phone_one')
        parent_phone_two = request.POST.get('parent_phone_two')
        emergency_person_first_name = request.POST.get('emergency_person_first_name')
        emergency_person_last_name = request.POST.get('emergency_person_last_name')
        emergency_person_phone_two = request.POST.get('emergency_person_phone_two')
        emergency_person_relation = request.POST.get('emergency_person_relation')
        form = StudentContact(school_name=school_name, student_first_name=student_first_name,
                              student_last_name=student_last_name, grade_level=grade_level,
                              parents_first_name=parents_first_name, parents_last_name=parents_last_name,
                              parent_phone_one=parent_phone_one, parent_phone_two=parent_phone_two,
                              emergency_person_first_name=emergency_person_first_name,
                              emergency_person_last_name=emergency_person_last_name,
                              emergency_person_phone_two=emergency_person_phone_two,
                              emergency_person_relation=emergency_person_relation)
        form.save()

    return render(request, 'signup.html')


def custom_context(request):
    # Add your logic to retrieve the value you want to pass to the base.html template
    announcements = Announcement.objects.all()

    # Return the context variable as a dictionary
    return {"announcements": announcements}


def home(request):
    rating = Yelp.objects.first()
    if rating is not None:
        rating_value = rating.rating
        reviews_value = rating.reviews
    else:
        rating_value = None
        reviews_value = None

    context = {"rating": rating_value, "review": reviews_value}

    return render(request, 'home.html', context)


def blog(request):
    return render(request, 'Blog.html')


def schedule(request):
    return render(request, 'schedule.html')


def partners(request):
    return render(request, 'Partners.html')


def team(request):
    return render(request, 'Team.html')


def signup(request):
    mydata = Event.objects.all()
    template = loader.get_template('Signup.html')
    context = {
        'mymembers': list(mydata),
    }
    return HttpResponse(template.render(context, request))


def message_for_contact(coach, name, email, message):
    contact_message = """
Dear {},

{} has contacted you with following message:

Email: {}
Message: {}

Best regards,

Great Knight Chess
""".format(coach, name, email, message)
    return contact_message


def contact(request):
    if request.method == 'POST':
        mydata = json.loads(request.body)
        model = ContactUs(
            name=mydata['name'],
            email=mydata['email'],
            message=mydata['message'],
        )
        model.save()
        message1 = message_for_contact("Seth", mydata['name'], mydata['email'], mydata['message'])
        message2 = message_for_contact("Shaun", mydata['name'], mydata['email'], mydata['message'])
        send_email("coachseth@greatknightschess.com", "New Contact Inquiry Received", message1)
        send_email("shaunlowney@greatknightschess.com", "New Contact Inquiry Received", message2)
        return JsonResponse({'status': '200'})
    return render(request, 'Contact.html')


def flayers(request):
    return render(request, 'Flyers.html')


def products(request):
    mydata = Product.objects.filter(quantity__gt=0).values()
    template = loader.get_template('Products.html')
    context = {
        'myproducts': mydata,
    }
    return HttpResponse(template.render(context, request))


def b_details(request):
    return render(request, 'B-detail.html')


def b_details2(request):
    return render(request, 'blog2.html')


def chess(request):
    return render(request, 'chess.html')

def product_detail(request, id):
    product = Product.objects.all().values().filter(id=id)
    products = Product.objects.get(id=id)
    template = loader.get_template('productDetail.html')
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        total = int(quantity) * products.price
        data = {
            'quantity': quantity,
            'product_id': id,
            'products': product,
            'total': total
        }
        return render(request, "productForm.html", data)
    context = {
        'products': product,
        'product_id': id
    }
    return HttpResponse(template.render(context, request))


def product_form(request):
    mydata = Product.objects.all().values()
    template = loader.get_template('productForm.html')
    context = {
        'products': mydata,
    }
    return HttpResponse(template.render(context, request))


def payment(request):
    mydata = Product.objects.all().values()
    template = loader.get_template('payment.html')
    context = {
        'product': mydata,
    }
    return HttpResponse(template.render(context, request))
