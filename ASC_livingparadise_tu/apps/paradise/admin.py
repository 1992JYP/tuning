from django.contrib import admin
from .models import Product, Review, Employees,NvProduct,NvReview

admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Employees)
admin.site.register(NvReview)
admin.site.register(NvProduct)

