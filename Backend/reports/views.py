from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from accounts.models import Profile
from .models import Report
from .serializers import ReportCreateSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_report(request):
    reporter_profile = get_object_or_404(Profile, user=request.user)

    serializer = ReportCreateSerializer(data=request.data)

    if serializer.is_valid():
        reported_profile = serializer.validated_data["reported_profile"]

        if reporter_profile == reported_profile:
            return Response(
                {"detail": "You cannot report yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )

        report = serializer.save(reporter=reporter_profile)

        return Response(
            {
                "message": "Report submitted successfully.",
                "report": ReportCreateSerializer(report).data
            },
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)