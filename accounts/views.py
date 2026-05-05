from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework import viewsets, permissions, generics
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import User
from .serializers import UserSerializer

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'admin')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class GoogleLogin(SocialLoginView):
    """
    Accepts a Google authorization code from the frontend (auth-code flow).
    The backend exchanges the code for tokens directly with Google.
    callback_url must be "postmessage" for popup-based auth.
    """
    adapter_class = GoogleOAuth2Adapter
    callback_url = "postmessage"
    client_class = OAuth2Client

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_object(self):
        return self.request.user
