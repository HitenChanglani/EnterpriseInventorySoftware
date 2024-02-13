from Items.models import Item, Category, Tag
from Items.serializers import ItemSerializer, TagSerializer, CategorySerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view


# Create your views here.

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated]) 
def item_views(request): 
    if request.method == 'GET': 
        if (len(request.query_params)) > 0:
            return get_filtered_items(request)
        return get_all_items() 
    elif request.method == 'POST':
        return add_item(request)


def get_all_items():
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)


def get_filtered_items(request):
    params = request.query_params
    items = Item.objects.all()

    for key in params.keys():
        if key.lower() == "category":
            categoryObj = Category.objects.filter(name=params[key])
            if categoryObj and len(categoryObj) > 0:
                items = items.filter(category=categoryObj[0].id)
            else:
                items = None
                break
        elif key.lower() == "status":
            items = items.filter(status=params[key])
        elif key.lower() == "fromdate":
            items = items.filter(updatedAt__gte=params[key])
        elif key.lower() == "todate":
            items = items.filter(updatedAt__lte=params[key])
        else:
            items = None
            break   
    
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)


def add_item(request): 
    serializer = ItemSerializer(data = request.data)
    try:
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": str(e)}, status = status.HTTP_400_BAD_REQUEST)
    
    

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated]) 
def category_views(request): 
    if request.method == 'GET': 
        return get_all_categories() 
    elif request.method == 'POST':
        return add_category(request)


def get_all_categories():
    items = Category.objects.all()
    serializer = CategorySerializer(items, many=True)
    return Response(serializer.data)


def add_category(request): 
    serializer = CategorySerializer(data = request.data) 
    try:
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": str(e)}, status = status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def tag_views(request): 
    if request.method == 'GET': 
        return get_all_tags() 
    elif request.method == 'POST':
        return add_tag(request)


def get_all_tags():
    items = Tag.objects.all()
    serializer = TagSerializer(items, many=True)
    return Response(serializer.data)


def add_tag(request): 
    serializer = TagSerializer(data = request.data) 
    try:
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": str(e)}, status = status.HTTP_400_BAD_REQUEST)