from rest_framework import permissions, generics, status
from rest_framework.response import Response
from .serializers import (
    CreateUserSerializer,
    UserSerializer,
    LoginUserSerializer,
    DuplicateEmailSerializer,
    DuplicateUserIdSerializer,
)
from knox.models import AuthToken
from .models import CustomUser
from django.core.mail import EmailMultiAlternatives
import random
import string

code = ''

class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        if len(request.data["username"]) < 6 or len(request.data["password"]) < 4:
            body = {"message": "short field"}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )

class DuplicateEmailAPI(generics.GenericAPIView):
    serializer_class = DuplicateEmailSerializer

    def post(self, request, *args, **kwargs):
        userList = CustomUser.objects.all()

        for user in userList:
            if(user.email == request.data["email"]) :
                body = {"message": "duplicate email address"}
                return Response(body, status=status.HTTP_400_BAD_REQUEST)

        global code
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

        subject, from_email, to = '1CL 인증번호 발송 메일입니다.', 'dvmflstm@gmail.com', request.data["email"]
        text_content = '1CL 회원가입 인증번호 : ' + code
        html_content = '<p>1CL 회원가입 인증번호 :<strong>' + code + '</strong></p>'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return Response(status=status.HTTP_204_NO_CONTENT)

class CodeVerificationAPI(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        global code
        if code != request.data["code"]:
            body = {"message": "code verification failed"}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)

class DuplicateUserIdAPI(generics.GenericAPIView):
    serializer_class = DuplicateUserIdSerializer

    def post(self, request, *args, **kwargs):
        userList = CustomUser.objects.all()

        for user in userList:
            if(user.username == request.data["username"]) :
                body = {"message": "duplicate user ID"}
                return Response(body, status=status.HTTP_400_BAD_REQUEST)


        return Response(status=status.HTTP_204_NO_CONTENT)

class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
