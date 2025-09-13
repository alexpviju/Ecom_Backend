from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import User, PasswordResetOTP


class SignupSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "confirm_password", "phn_num"]

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")  # not needed for DB

        # ✅ Hash password before saving
        validated_data["password"] = make_password(validated_data["password"])

        return User.objects.create(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "User not found"})

        # ✅ Compare hashed password
        if not check_password(data["password"], user.password):
            raise serializers.ValidationError({"password": "Invalid password"})

        data["user"] = user
        return data


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No account found with this email")
        return value


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
            otp_obj = PasswordResetOTP.objects.filter(user=user, otp=data['otp'], is_used=False).latest('created_at')
        except (User.DoesNotExist, PasswordResetOTP.DoesNotExist):
            raise serializers.ValidationError({"otp": "Invalid or expired OTP"})

        data['user'] = user
        data['otp_obj'] = otp_obj
        return data


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match"})

        try:
            user = User.objects.get(email=data['email'])
            otp_obj = PasswordResetOTP.objects.filter(
                user=user, otp=data['otp'], is_used=False
            ).latest('created_at')
        except (User.DoesNotExist, PasswordResetOTP.DoesNotExist):
            raise serializers.ValidationError({"otp": "Invalid or expired OTP"})

        data['user'] = user
        data['otp_obj'] = otp_obj
        return data

    def save(self, **kwargs):
        user = self.validated_data['user']
        otp_obj = self.validated_data['otp_obj']

        # ✅ Securely hash password
        user.password = make_password(self.validated_data['new_password'])
        user.save()

        # Mark OTP as used
        otp_obj.is_used = True
        otp_obj.save()

        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = self.context["request"].user  # current logged-in user

        # ✅ check old password
        if not check_password(data["old_password"], user.password):
            raise serializers.ValidationError({"old_password": "Old password is incorrect"})

        # ✅ check match
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError({"password": "Passwords do not match"})

        return data

    def save(self, **kwargs):
        user = self.context["request"].user

        # ✅ hash new password before saving
        user.password = make_password(self.validated_data["new_password"])
        user.save()

        return user