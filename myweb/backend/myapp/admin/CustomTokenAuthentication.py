from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from ..database.TokenFactory import TokenFactory  # Import your TokenFactory class
from ..models import User
import jwt
from django.conf import settings

class CustomTokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        # Get the token from the 'Authorization' header
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return None

        token = token.split(' ')[1]

        # Use TokenFactory's check_token method to check the token
        token_check_result = TokenFactory.check_token(token)

        

        if not token_check_result:
            raise AuthenticationFailed('Invalid token.')

        print(token)

        # If token is valid, get the user
        try:
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            userid = decoded.get('user_id')
            user = User.objects.get(userid=userid)  # Retrieve the User instance
        except User.DoesNotExist:
            raise AuthenticationFailed('No user matching this token was found.')

        return (user, token)
