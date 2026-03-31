from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer
from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.
@api_view(['POST'])
def admin_signup(request):
    data = request.data.copy()
    data['roles'] = 'admin'

    serializer = SignupSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"Admin created successfully"}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def sales_executive_signup(request):
    data = request.data.copy()
    data['roles'] = 'sales'

    serializer = SignupSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"Sales Executive created successfully"}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def inventory_manager_signup(request):
    data = request.data.copy()
    data['roles'] = 'inventory'

    serializer = SignupSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"Inventory Manager created successfully"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def custom_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(username=email, password=password)
    
    if user is not None:
        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Login successful",
            "roles": user.roles,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })
    
    return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def get_users(request):
    users = CustomUser.objects.all().values('id', 'email', 'roles')
    return Response(users)