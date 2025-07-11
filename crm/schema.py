import graphene
from graphene_django.types import DjangoObjectType
from .models import Product

class ProductType(DjangoObjectType):
    class Meta:
        model = Product

class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass  # No arguments needed for this mutation

    products = graphene.List(ProductType)
    message = graphene.String()

    def mutate(self, info):
        # Get products with stock < 10
        low_stock_products = Product.objects.filter(stock__lt=10)
        
        # Update stock for each product
        updated_products = []
        for product in low_stock_products:
            product.stock += 10  # Increment stock by 10
            product.save()
            updated_products.append(product)
        
        return UpdateLowStockProducts(
            products=updated_products,
            message=f"Successfully updated {len(updated_products)} low-stock products"
        )

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()
    