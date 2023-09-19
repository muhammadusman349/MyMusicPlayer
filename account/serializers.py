from .models import User
from rest_framework import serializers,status
from rest_framework_simplejwt.tokens import RefreshToken

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type":"password"},write_only = True)

    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'email',
            'phone',
            'password',
            'password2',
            'created_at',
            'updated_at',
        )
        read_only_fields=["created_at","updated_at"]
        extra_kwargs = {
                    'password':{'write_only':True},
        }

    def validate(self, obj):
        if obj['password'] != obj['password2']:
            raise serializers.ValidationError({"Password": "Password fields didn't match."})
        return obj
    
    def create(self,validated_data):   
        user_obj = User(
            name      = validated_data.get('name'),
            email     = validated_data.get('email'),
            phone     = validated_data.get('phone'),
            )
                  
        user_obj.set_password(validated_data.get('password'))
        user_obj.save()
        return user_obj

class Loginserializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password  =serializers.CharField(required=True)
     
    def validate(self, attr):
        email = attr.get('email', '')
        password = attr.get('password', '')
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"email": "provided credentials are not valid email"}, code=status.HTTP_401_UNAUTHORIZED)

        if user:
            if not user.check_password(password):
                raise serializers.ValidationError(
                    {"password": "provided credentials are not valid password"}, code=status.HTTP_401_UNAUTHORIZED)
                
        token = RefreshToken.for_user(user)
        attr['id']            = int(user.id)
        attr['name']          = str(user.name)
        attr['email']         = str(user.email)
        attr['access_token']  = str(token.access_token)
        attr['refresh_token'] = str(token)
        
        return attr