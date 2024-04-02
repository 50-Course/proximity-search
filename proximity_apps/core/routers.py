from rest_framework.routers import SimpleRouter

from proximity_apps.core.views import (RefreshViewset, SignInViewset,
                                       SignUpViewset)

router =  SimpleRouter()

router.register(r'auth/login', SignInViewset, basename='auth-login')
router.register(r'auth/signup', SignUpViewset, basename='auth-signup')
router.register(r'auth/refresh', RefreshViewset, basename='auth-refresh')
