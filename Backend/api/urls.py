from django.urls import path
from .views import (
    hello,
    ProviderApplicationViewSet,
    ProviderViewSet,
    ProviderApplicationUploadCredentialView,
    AdminProviderApplicationReviewView,
)

urlpatterns = [
    path("", hello),

    # user endpoints
    path("provider/applications/me/", ProviderApplicationViewSet.as_view()),
    path("provider/applications/", ProviderViewSet.as_view()),
    path("provider/applications/me/credentials/", ProviderApplicationUploadCredentialView.as_view()),

    # admin endpoint
    path("admin/provider/applications/<int:pk>/", AdminProviderApplicationReviewView.as_view()),
]