from django.conf import settings

def access_oauth2_settings(request):
    """Allows to use selected settings in a template"""
    return {
        'SOCIAL_AUTH_VK_OPENAPI_APP_ID': settings.SOCIAL_AUTH_VK_OPENAPI_APP_ID,
        'SOCIAL_AUTH_VK_COMPLETE_URL': settings.SOCIAL_AUTH_VK_COMPLETE_URL
    }