# jobs/views.py
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import Job
from .serializers import JobCreateSerializer, JobSerializer, JobUpdateSerializer
from accounts.models import ServiceProvider, Profile
from haversine import haversine, Unit

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_job(request):

    serializer = JobCreateSerializer(
        data=request.data,
        context={"request": request}
    )

    profile = Profile.objects.get(user=request.user)

    data = request.data.copy()

    data["latitude"] = data.get("latitude") or profile.latitude
    data["longitude"] = data.get("longitude") or profile.longitude

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


@api_view(["GET"])
def search_jobs(request):
    jobs = Job.objects.all()

    # Filter by services
    services = request.GET.get("services")
    if services:
        service_ids = services.split(",")
        jobs = jobs.filter(services__id__in=service_ids).distinct()

    # Filter by budget
    min_budget = request.GET.get("budget")
    if min_budget:
        jobs = jobs.filter(budget__gte=min_budget)

    # Filter by request type
    request_type = request.GET.get("request_type")
    if request_type:
        jobs = jobs.filter(request_type=request_type)

    # Filter by location
    max_distance = request.GET.get("max_distance")
    if max_distance and request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        user_coord = (profile.latitude, profile.longitude)

        jobs = [job for job in jobs if haversine(user_coord, (job.latitude, job.longitude), unit=Unit.MILES) <= float(max_distance)]

    serializer = JobSerializer(jobs, many=True, context={"request": request})
    return Response(serializer.data)