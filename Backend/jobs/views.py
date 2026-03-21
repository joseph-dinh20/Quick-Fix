# jobs/views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import Job
from .serializers import JobCreateSerializer, JobSerializer
from accounts.models import ServiceProvider


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

    serializer = JobSerializer(jobs, many=True, context={"request": request})
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_favorites(request):
    try:
        service_provider = ServiceProvider.objects.get(profile__user=request.user)
    except ServiceProvider.DoesNotExist:
        return Response({"error": "Not a service provider"}, status=403)

    jobs = service_provider.favorited_jobs.all()
    serializer = JobSerializer(jobs, many=True, context={"request": request})
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def toggle_favorite(request, job_id):
    try:
        service_provder = ServiceProvider.objects.get(profile__user=request.user)
    except ServiceProvider.DoesNotExist:
        return Response({"error": "Not a service provider"}, status=403)

    job = Job.objects.get(id=job_id)

    if service_provder.favorited_jobs.filter(id=job.id).exists():
        service_provder.favorited_jobs.remove(job)
        return Response({"favorited": False})
    else:
        service_provder.favorited_jobs.add(job)
        return Response({"favorited": True})
    

@api_view(["GET"])
@permission_classes([AllowAny])
def list_jobs(request):
    jobs = Job.objects.all().order_by("-id")  # newest jobs first

    serializer = JobSerializer(
        jobs,
        many=True,
        context={"request": request}
    )
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_job(request, job_id):
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return Response({"error": "Job not found"}, status=404)

    if job.customer.user != request.user:
        return Response({"error": "Not allowed"}, status=403)

    job.delete()
    return Response({"success": True})