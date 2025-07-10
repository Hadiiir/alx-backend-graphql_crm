import graphene
from graphene_django import DjangoObjectType
from django.db.models import Sum
from .models import Customer, Product, Order

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = "__all__"

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = "__all__"

class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass

    updated_products = graphene.List(ProductType)
    success_message = graphene.String()
    count = graphene.Int()

    def mutate(self, info):
        # Query products with stock < 10
        low_stock_products = Product.objects.filter(stock__lt=10)
        
        updated_products = []
        for product in low_stock_products:
            # Increment stock by 10
            product.stock += 10
            product.save()
            updated_products.append(product)
        
        success_message = f"Successfully updated {len(updated_products)} low-stock products"
        
        return UpdateLowStockProducts(
            updated_products=updated_products,
            success_message=success_message,
            count=len(updated_products)
        )

class Query(graphene.ObjectType):
    customers = graphene.List(CustomerType)
    products = graphene.List(ProductType)
    orders = graphene.List(OrderType)
    
    # CRM Report queries
    total_customers = graphene.Int()
    total_orders = graphene.Int()
    total_revenue = graphene.Float()
    
    def resolve_customers(self, info):
        return Customer.objects.all()
    
    def resolve_products(self, info):
        return Product.objects.all()
    
    def resolve_orders(self, info):
        return Order.objects.all()
    
    def resolve_total_customers(self, info):
        return Customer.objects.count()
    
    def resolve_total_orders(self, info):
        return Order.objects.count()
    
    def resolve_total_revenue(self, info):
        total = Order.objects.aggregate(Sum('totalamount'))['totalamount__sum']
        return total or 0.0

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)