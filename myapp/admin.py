from django.contrib import admin
from .models import School, Event, Session, Product, ProductSale, ServicesSale, ContactUs, Yelp, Announcement


class StudentContactAdmin(admin.ModelAdmin):
    list_display = (
        "school_name", "student_first_name", "student_last_name", "grade_level", "parents_first_name",
        "parents_last_name",
        "parent_phone_one", "parent_phone_two", "emergency_person_first_name", "emergency_person_last_name",
        "emergency_person_phone_two", "emergency_person_relation")
    list_filter = ("school_name", "grade_level")
    search_fields = (
        "school_name", "student_first_name", "student_last_name", "grade_level", "parents_first_name",
        "parents_last_name",
        "parent_phone_one", "parent_phone_two", "emergency_person_first_name", "emergency_person_last_name",
        "emergency_person_phone_two", "emergency_person_relation")


class ProductSaleAdmin(admin.ModelAdmin):
    list_display = (
        "product_name", "price", "quantity", "total", "email", "phone_number", "first_name", "last_name", "country",
        "street", "apt", "postal_code", "city",
        "transaction")
    search_fields = (
        "product__product_name","product__price","quantity","email", "phone_number", "first_name", "last_name", "country", "street", "apt", "postal_code", "city", "total")
    list_filter = ("product__product_name","product__price","email", "country", "postal_code", "city", "transaction__payment_status")

    @admin.display(description='Transaction Status', ordering="transaction__payment_status")
    def transaction(self, object):
        return object.transaction.payment_status

    @admin.display(description='Price', ordering="product__price")
    def price(self, object):
        return object.product.price

    @admin.display(description='Product Name', ordering="product__product_name")
    def product_name(self, object):
        return object.product.product_name


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "product_name",
        "image",
        "price",
        "description",
    )
    search_fields = (
        "product_name",
        "price",
        "description"
    )


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "payment_status",
    )
    search_fields = (
        "payment_status",
    )
    list_filter = (
        "payment_status",
    )


class ServicesSaleAdmin(admin.ModelAdmin):
    list_display = (
        "school_name",
        "session",
        "duration",
        "price",
        "instructor_name",
        "transaction",
        "st_first_name",
        "st_last_name",
        "grade_level",
        "pr_first_name",
        "pr_last_name",
        "phone_number_one",
        "phone_number_two",
        "email",
        "emr_first_name",
        "emr_last_name",
        "emr_phone_number",
        "relation",
    )

    @admin.display(description='School Name', ordering="event__school_name")
    def school_name(self, object):
        return object.event.school_name

    @admin.display(description='Transaction Status', ordering="transaction__payment_status")
    def transaction(self, object):
        return object.transaction.payment_status

    @admin.display(description='Session', ordering="event__session")
    def session(self, object):
        return object.event.session

    @admin.display(description='Duration', ordering="event__duration")
    def duration(self, object):
        return object.event.duration

    @admin.display(description='Price', ordering="event__price")
    def price(self, object):
        return object.event.price

    @admin.display(description='Instructor Name', ordering="event__instructor_name")
    def instructor_name(self, object):
        return object.event.instructor_name

    search_fields = (
        "st_first_name",
        "st_last_name",
        "grade_level",
        "pr_first_name",
        "pr_last_name",
        "phone_number_one",
        "phone_number_two",
        "emr_first_name",
        "emr_last_name",
        "emr_phone_number",
        "relation",
        "amount_paid",
        "event__school_name__school_name",
        "event__duration",
        "event__session__session",
        "event__instructor_name",
        "event__price",
        "email",
        "transaction__payment_status",
    )
    list_filter = (
        "grade_level",
        "event__school_name__school_name",
        "event__duration",
        "event__session__session",
        "event__instructor_name",
        "event__price",
        "email",
        "transaction__payment_status",
    )


class EventAdmin(admin.ModelAdmin):
    list_display = (
        "school_name",
        "session",
        "duration",
        "price",
        "instructor_name",
    )
    search_fields = (
        "school_name__school_name",
        "session__label",
        "duration",
        "price",
        "instructor_name",
    )
    list_filter = (
        "school_name",
        "session",
        "duration",
        "price",
        "instructor_name",
    )


class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "message",
    )


admin.site.register(Event, EventAdmin)
admin.site.register(School)
admin.site.register(Session)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductSale, ProductSaleAdmin)
admin.site.register(ServicesSale, ServicesSaleAdmin)
admin.site.register(ContactUs, ContactAdmin)
admin.site.register(Yelp)
admin.site.register(Announcement)
