from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Job
from .serializers import JobUpdateSerializer


@api_view(["PATCH", "PUT"])
@permission_classes([IsAuthenticated])
def update_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if job.customer.user != request.user:
        return Response(
            {"detail": "You do not have permission to edit this job."},
            status=status.HTTP_403_FORBIDDEN
        )

    serializer = JobUpdateSerializer(job, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "message": "Job updated successfully.",
                "job": serializer.data
            },
            status=status.HTTP_200_OK
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)