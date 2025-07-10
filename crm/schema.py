import graphene
from graphene_django import DjangoObjectType
from products.models import Product

class ProductType(DjangoObjectType):
    class Meta:
        model = Product

class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass  # No arguments needed

    products = graphene.List(ProductType)
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info):
        # Get products with stock < 10
        low_stock_products = Product.objects.filter(stock__lt=10)
        
        # Update stock levels
        updated_products = []
        for product in low_stock_products:
            product.stock += 10
            product.save()
            updated_products.append(product)
        
        return UpdateLowStockProducts(
            products=updated_products,
            message=f"Updated {len(updated_products)} products"
        )

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()

# Add to your existing schema
schema = graphene.Schema(mutation=Mutation)