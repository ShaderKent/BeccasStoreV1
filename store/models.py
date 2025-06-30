from django.db import models
from django.urls import reverse

from category.models import Category

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    description_short = models.CharField(max_length=200, blank=True)
    description_full = models.TextField(max_length=500, blank=True)
    slug = models.CharField(max_length=200, unique=True)
    price = models.FloatField()
    stock = models.IntegerField()
    image1 = models.ImageField(upload_to="photos/products", blank=True)
    image2 = models.ImageField(upload_to="photos/products", blank=True)
    image3 = models.ImageField(upload_to="photos/products", blank=True)
    image4 = models.ImageField(upload_to="photos/products", blank=True)
    image5 = models.ImageField(upload_to="photos/products", blank=True)
    image6 = models.ImageField(upload_to="photos/products", blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
    created_date = models.DateTimeField(auto_now_add = True)
    modified_date = models.DateTimeField(auto_now = True)
    is_available = models.BooleanField(default=True)

    def get_image_url(self, requested_image):
        try:
            image = requested_image
            if image:
                return image
        except: 
            return "#"

    
    def __str__(self):
        return self.product_name