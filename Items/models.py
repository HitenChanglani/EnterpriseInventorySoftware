from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length = 64, unique=True)


class Tag(models.Model):
    name = models.CharField(max_length = 32, unique=True)


class Item(models.Model):
    statusChoices = (('OUT_OF_STOCK', 'OUT_OF_STOCK'), ('IN_STOCK', 'IN_STOCK'))

    sku = models.CharField(max_length = 32, unique=True)
    name = models.CharField(max_length = 64)
    availableStock = models.PositiveIntegerField()
    status = models.CharField(max_length = 16, choices = statusChoices, default = 'IN_STOCK')
    category = models.ForeignKey("Items.Category", on_delete = models.CASCADE, null = False)
    tags = models.ManyToManyField(Tag)
    createdAt = models.DateField(auto_now_add=True)
    updatedAt = models.DateField(auto_now=True)
