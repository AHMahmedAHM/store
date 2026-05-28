from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status 
from .serializers import ProductSerializer
from .models import Product
from django.views.decorators.csrf import csrf_exempt

@api_view(['GET'])
def api_products_list(request):
    "api view to show all available products "
    # get products
    products = Product.objects.filter(available=True)
    #turn it to JSON
    serializer = ProductSerializer(products, many=True)

    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAdminUser])
def api_add_product(request):
    'api view to add products'

    if not request.data :
        return Response ({"message":'info not input'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ProductSerializer(data= request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else :
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def api_delete_product(request, product_id):
    'api view to delete product'

    try :
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist :
        return Response({'error' : 'product not found'}, status=status.HTTP_404_NOT_FOUND)
    
    product.delete()
    return Response(status = status.HTTP_204_NO_CONTENT)##204 لا اي رسائل 


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminUser])
def api_update_product(request, product_id):
    'api view to partial and full update for products'

    if not request.data :
        return Response ({"message":'info not input'}, status=status.HTTP_400_BAD_REQUEST)


    try :
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error':'product not found'}, status=status.HTTP_404_NOT_FOUND)

    is_partial = request.method == 'PATCH'

    ###maybe  : ProductSerializer(product, data=request.data) positional argument 
    serializer = ProductSerializer(data = request.data, instance=product, partial =is_partial)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
