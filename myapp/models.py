from django.db import models

GRADE_LEVEL = (
    ("one", "One"),
    ("two", "Two"),
    ("three", "Three"),
    ("four", "Four"),

)

Status = (
    ("INITIATED", "INITIATED"),
    ("SUCCEEDED", "SUCCEEDED"),
    ("FAILED", "FAILED"),
)

Type = (
    ("PRODUCTS", "PRODUCTS"),
    ("SERVICES", "SERVICES"),
)


#
# class Product(models.Model):
#     name = models.CharField(max_length=100)
#     price = models.DecimalField(max_digits=6, decimal_places=2)
#
#     def __str__(self):
#         return self.name


class StudentContact(models.Model):
    school_name = models.CharField(max_length=255)
    student_first_name = models.CharField(max_length=255)
    student_last_name = models.CharField(max_length=255)
    grade_level = models.CharField(max_length=255, choices=GRADE_LEVEL, default='Select Your Level')
    parents_first_name = models.CharField(max_length=255, null=True)
    parents_last_name = models.CharField(max_length=255, null=True)
    parent_phone_one = models.CharField(max_length=13)
    parent_phone_two = models.CharField(max_length=13)
    emergency_person_first_name = models.CharField(max_length=255)
    emergency_person_last_name = models.CharField(max_length=255)
    emergency_person_phone_two = models.CharField(max_length=13)
    emergency_person_relation = models.CharField(max_length=255)

    def __str__(self):
        return self.student_first_name + " (" + self.school_name + ")"


class Yelp(models.Model):
    rating = models.FloatField()
    reviews = models.IntegerField()

    def __str__(self):
        return "rating"


class School(models.Model):
    school_name = models.CharField(max_length=255)

    def __str__(self):
        return self.school_name


class Session(models.Model):
    session = models.CharField(max_length=255)

    def __str__(self):
        return self.session


class Event(models.Model):
    school_name = models.ForeignKey(School, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    duration = models.CharField(max_length=20, default="1 hr")
    price = models.IntegerField()
    instructor_name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.school_name) + " - " + str(self.session)


class ServiceTransaction(models.Model):
    payment_status = models.CharField(max_length=255, choices=Status, default='INITIATED')

    def __str__(self):
        return str(self.payment_status)


class ProductTransaction(models.Model):
    payment_status = models.CharField(max_length=255, choices=Status, default='INITIATED')

    def __str__(self):
        return str(self.payment_status)


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media/images/')
    price = models.IntegerField()
    quantity = models.IntegerField()
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.product_name


class ProductSale(models.Model):
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=12)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    apt = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=12)
    city = models.CharField(max_length=255)
    product = models.ForeignKey(Product, related_name='product', on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False)
    total = models.IntegerField()
    transaction = models.ForeignKey(ProductTransaction, related_name='product_transaction', on_delete=models.CASCADE)

    def __str__(self):
        return self.email


class ServicesSale(models.Model):
    st_first_name = models.CharField(max_length=255)
    st_last_name = models.CharField(max_length=255)
    grade_level = models.CharField(max_length=255)
    pr_first_name = models.CharField(max_length=255)
    pr_last_name = models.CharField(max_length=255)
    phone_number_one = models.CharField(max_length=12)
    phone_number_two = models.CharField(max_length=12)
    email = models.EmailField(max_length=254)
    emr_first_name = models.CharField(max_length=255)
    emr_last_name = models.CharField(max_length=255)
    emr_phone_number = models.CharField(max_length=12)
    relation = models.CharField(max_length=255)
    event = models.ForeignKey(Event, related_name='event', on_delete=models.CASCADE)
    amount_paid = models.IntegerField()
    transaction = models.ForeignKey(ServiceTransaction, related_name='transaction', on_delete=models.CASCADE)

    def __str__(self):
        return self.st_first_name


class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    message = models.TextField()

    class Meta:
        verbose_name_plural = "Contact Us"

    def __str__(self):
        return self.name


class Announcement(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text
