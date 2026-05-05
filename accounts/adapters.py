from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        """
        Populates user fields from social provider data.
        """
        user = super().populate_user(request, sociallogin, data)
        
        # Google specific mapping
        if sociallogin.account.provider == 'google':
            name = data.get('name')
            if not name:
                first_name = data.get('given_name', '')
                last_name = data.get('family_name', '')
                name = f"{first_name} {last_name}".strip()
            
            if name:
                user.full_name = name
            
            picture = data.get('picture')
            if picture:
                user.profile_image_url = picture
                
        return user

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        # Ensure full_name is saved if it was populated
        if hasattr(user, 'full_name') and not user.full_name:
            # Last resort fallback to email part
            user.full_name = user.email.split('@')[0]
        user.save()
        return user
