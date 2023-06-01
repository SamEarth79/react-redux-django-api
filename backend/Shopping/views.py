from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer
from rest_framework import status
from django.contrib.auth import authenticate


@api_view(["GET"])
def getUsers(request):
    users = User.objects.all()
    allUsers = {}
    for user in users:
        allUsers[user.id] = {"username": user.username, "password": user.password}

    return Response(allUsers)


@api_view(["POST"])
def SignUp(request):
    print(request.data)
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def LogIn(request):
    print(request.data)
    user = User.objects.filter(username=request.data["username"])
    if not user.exists():
        return Response(
            {"returnMsg": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST
        )

    # user = authenticate(username=username, password=password)
    # if user is None:

    if user[0].password != request.data["password"]:
        return Response(
            {"returnMsg": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST
        )

    return Response(
        {
            "returnMsg": "Valid Credentials",
            "userData": {
                "id": user[0].id,
                "username": user[0].username,
                # "password": user[0].password,
            },
        },
        status=status.HTTP_202_ACCEPTED,
    )


# {
# "username":"sam",
# "password":"sam"
# }
