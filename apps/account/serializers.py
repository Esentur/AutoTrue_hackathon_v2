from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.core.mail import send_mail

from apps.account.models import MyUser
from apps.purchase.serializers import PurchaseSerializer

User = get_user_model()


def send_active_mail(code, email, username):
    full_link = f'http://localhost:8000/account/active/{code}/'
    send_mail(
        "Ваш активационный код",
        f"Здравствуйте {username.title()}.\n Пожалуйста перейдите по ссылке: {full_link} \n для активации вашего аккаунта.",
        'sulimanovuran@gmail.com',
        [email]
    )


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(min_length=6, write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, attrs):
        p = attrs.get('password')
        p2 = attrs.pop('password2')

        if p != p2:
            raise serializers.ValidationError('Пароли не совпадают!')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        code = user.activation_code
        send_active_mail(code, user.email, user.username)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Нет такого пользователя')
        return email

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Данные введены не корректно')
            attrs['user'] = user
            return attrs


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        purchases=[]
        for purchas in instance.purchases.all():
            print(purchas)
            purchases.append(str(purchas))
        representation['Заказы'] = purchases
        return representation


class ResetPasswordSerilizer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не зарегистрирован')
        return email

    def send_reset_password_link(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.generate_activation_code()
        user.save()
        password_recovery_code = user.activation_code

        send_mail(
            'Восстановление пароля',
            f'Здравсвуйте {user.username}.\nВаш код для восстановления пароля\n{password_recovery_code}',
            'sulaimanovuran@gmail.com',
            [email]
        )


class CreateNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(min_length=8, max_length=40, required=True)
    password = serializers.CharField(required=True)
    password_confirm = serializers.CharField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не зарегистрирован')
        return email

    def validate_code(self, code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('Пользователь не зарегистрирован')
        return code

    def validate(self, attrs):
        pass1 = attrs.get('password')
        pass2 = attrs.get('password_confirm')
        if pass1 != pass2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def set_new_pass(self):
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        user = User.objects.get(email=email)

        user.set_password(password)
        user.activation_code = ''
        user.save()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    password = serializers.CharField(required=True, min_length=6)
    password_confirm = serializers.CharField(required=True, min_length=6)

    def validate_old_password(self, old_password):
        user = self.context.get('request').user
        if not user.check_password(old_password):
            raise serializers.ValidationError('Wrong password')
        return old_password

    def validate(self, attrs):
        password1 = attrs.get('password')
        password2 = attrs.get('password_confirm')
        if password1 != password2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def set_new_password(self):
        user = self.context.get('request').user
        password = self.validated_data.get('password')
        user.set_password(password)
        user.save()


class PurchaseHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['purchase_history'] = PurchaseSerializer(instance.purchases.all(), many=True).data
        return representation
