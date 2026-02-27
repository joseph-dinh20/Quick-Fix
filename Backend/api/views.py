from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework import status
from django.utils import timezone
from accounts.models import Profile

from accounts.models import ProviderApplication
from .serializers import ProviderApplicationSerializer

# Create your views here.


@api_view(['GET'])
def hello(request):
    return Response({"message": "Hello from Django backend!"})

class ProviderApplicationViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        app = ProviderApplication.objects.filter(user=request.user).first()
        if not app:
            return Response({"detail": "No provider application found"}, status=404)
        return Response(ProviderApplicationSerializer(app).data)


class ProviderViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        existing = ProviderApplication.objects.filter(user=request.user).first()
        if existing:
            return Response(
                {"detail": "Provider application already exists.", "status": existing.status},
                status=400
            )

        serializer = ProviderApplicationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        app = ProviderApplication.objects.create(
            user=request.user,
            **serializer.validated_data
        )

        return Response(
            ProviderApplicationSerializer(app).data,
            status=status.HTTP_201_CREATED
        )


class ProviderApplicationUploadCredentialView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        app = ProviderApplication.objects.filter(user=request.user).first()
        if not app:
            return Response({"detail": "Create an application first."}, status=400)

        f = request.FILES.get("credential_file")
        if not f:
            return Response({"detail": "Credential file is required."}, status=400)

        if f.size > 10 * 1024 * 1024:
            return Response({"detail": "File is too large (max 10MB)."}, status=400)

        app.credential_file = f
        app.save()

        return Response(ProviderApplicationSerializer(app).data)


class AdminProviderApplicationReviewView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk: int):
        from accounts.models import Profile

        app = ProviderApplication.objects.filter(pk=pk).first()
        if not app:
            return Response({"detail": "NOT FOUND"}, status=404)

        new_status = request.data.get("status")
        notes = request.data.get("review_notes", "")

        if new_status not in [
            ProviderApplication.Status.PENDING,
            ProviderApplication.Status.APPROVED,
            ProviderApplication.Status.REJECTED,
        ]:
            return Response({"detail": "Invalid status."}, status=400)

        app.status = new_status
        app.review_notes = notes
        app.review_at = timezone.now()
        app.save()

        if app.status == ProviderApplication.Status.APPROVED:
            profile, _ = Profile.objects.get_or_create(
                user=app.user,
                defaults={"name": app.full_name}
            )
            profile.role = Profile.PROVIDER
            profile.save()

        return Response(ProviderApplicationSerializer(app).data)