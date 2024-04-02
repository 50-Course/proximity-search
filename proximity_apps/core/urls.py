from django.urls import include, path

from .routers import router as routes

urlpatterns = [
    path('api/', include(routes.urls))
]
