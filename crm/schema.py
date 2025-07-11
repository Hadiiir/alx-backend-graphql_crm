import graphene
from graphene_django.types import DjangoObjectType
from .models import Product

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ('id', 'name', 'stock')

class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass  # No arguments needed

    products = graphene.List(ProductType)
    message = graphene.String()

    def mutate(self, info):
        # Query products with stock < 10
        low_stock_products = Product.objects.filter(stock__lt=10)
        
        # Increment stock by 10 for each product
        updated_products = []
        for product in low_stock_products:
            product.stock += 10
            product.save()
            updated_products.append(product)
        
        return UpdateLowStockProducts(
            products=updated_products,
            message=f"Restocked {len(updated_products)} low-stock products"
        )

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()
    