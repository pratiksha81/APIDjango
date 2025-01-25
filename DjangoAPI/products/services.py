from .models import Product
from django.core.exceptions import ObjectDoesNotExist
from asgiref.sync import sync_to_async
from .serializers import ProductSerializer

class ProductService:
    
    async def get_all_products(self):
        products = await sync_to_async(list)(Product.objects.all())
        return ProductSerializer(products, many=True).data

    @staticmethod
    async def create_product(data):
        """
        Create a new product with the provided data.
        Returns a success flag and serialized product data or errors.
        """
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            product = await sync_to_async(serializer.save)()
            return {"success": True, "data": ProductSerializer(product).data}
        return {"success": False, "errors": serializer.errors}

    @staticmethod
    async def get_product_by_id(pk):
        """
        Fetch a single product by its primary key.
        Returns the product instance or None if not found.
        """
        try:
            product = await sync_to_async(Product.objects.get)(pk=pk)
            return product
        except Product.DoesNotExist:
            return None

    @staticmethod
    async def update_product(pk, data):
        """
        Update an existing product with the given data.
        Returns a success flag and serialized product data or errors.
        """
        product = await ProductService.get_product_by_id(pk)
        if not product:
            return {"success": False, "message": "Product not found."}

        serializer = ProductSerializer(product, data=data)
        if serializer.is_valid():
            await sync_to_async(serializer.save)()
            return {"success": True, "data": serializer.data}
        return {"success": False, "errors": serializer.errors}

    @staticmethod
    async def delete_product(pk):
        """
        Delete a product by its primary key.
        Returns a success flag and a message.
        """
        product = await ProductService.get_product_by_id(pk)
        if not product:
            return {"success": False, "message": "Product not found."}

        await sync_to_async(product.delete)()
        return {"success": True, "message": "Product deleted successfully."}
