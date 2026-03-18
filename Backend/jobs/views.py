# jobs/views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Job
from .serializers import JobCreateSerializer, JobSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_job(request):

    serializer = JobCreateSerializer(
        data=request.data,
        context={"request": request}
    )

    if serializer.is_valid():
        job = serializer.save()
        return Response({"id": job.id}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_jobs(request):
    profile = request.user.profile

    jobs = Job.objects.filter(customer=profile).order_by("-created_at")

    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)