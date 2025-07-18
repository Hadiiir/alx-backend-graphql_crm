import graphene
from graphene_django import DjangoObjectType
from products.models import Product  # Assuming you have a Product model

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "stock")

class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass  # No arguments needed

    products = graphene.List(ProductType)
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info):
        # Get products with stock < 10
        low_stock_products = Product.objects.filter(stock__lt=10)
        
        # Update stock by adding 10 to each
        updated_products = []
        for product in low_stock_products:
            product.stock += 10
            product.save()
            updated_products.append(product)
        
        return cls(
            products=updated_products,
            message=f"Updated {len(updated_products)} low-stock products"
        )

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()

# Add to your existing Schema class if you have one
# schema = graphene.Schema(mutation=Mutation)