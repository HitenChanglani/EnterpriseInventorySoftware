from .models import Item, Tag, Category
from django.forms import ValidationError
from rest_framework import serializers
from Items.functions import deserialize_json


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

    def create(self, validated_data):
        category = validated_data.get('name')
        category = deserialize_json(category, expect_type=str)
        validated_data['name'] = category

        instance = super().create(validated_data)
        return instance


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

    def create(self, validated_data):        
        tag = validated_data.get('name')
        tag = deserialize_json(tag, expect_type=str)
        validated_data['name'] = tag

        instance = super().create(validated_data)
        return instance
        
class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)  
    class Meta:
        model = Item
        fields = ['sku', 'name', 'availableStock', 'status', 'category', 'tags', 'createdAt', 'updatedAt']

    def create(self, validated_data):
        data = validated_data

        # User Provided Fields
        itemName = data.get('name')
        itemName = deserialize_json(itemName, expect_type=str)
        validated_data['name'] = itemName

        availableStock = data.get('availableStock')
        availableStock = deserialize_json(availableStock, expect_type=int)
        validated_data['availableStock'] = availableStock

        # Handled Fields
        categoryName = self.initial_data.get('category') 
        categoryName = deserialize_json(categoryName, expect_type=str)
        category = Category.objects.filter(name=categoryName)
        if not category or len(category)==0:
            raise ValidationError("Invalid category")
        validated_data["category_id"] = category[0].id

        tagStr = self.initial_data.get('tags')
        tagStr = tagStr.replace('"', '')
        tagStr = tagStr.replace("'", '')
        tags = tagStr.strip('][').split(', ')
        tags = deserialize_json(tags, expect_type=list)
        tagObjects = Tag.objects.filter(name__in=tags)
        tagIdDict = { tagObject.name : tagObject.id for tagObject in tagObjects }
        for tag in tags:
            if tag not in tagIdDict:
                newTag = Tag(name=tag)
                newTag.save()
                tagIdDict[tag] = newTag.id
            
        validated_data['tags'] = tagIdDict.values()

        if availableStock > 0:
            validated_data['status'] = "IN_STOCK"
        else:
            validated_data['status'] = "OUT_OF_STOCK"

        instance = super().create(validated_data)
        return instance
