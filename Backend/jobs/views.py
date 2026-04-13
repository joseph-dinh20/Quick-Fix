# jobs/views.py
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, NotFound
from django.db.models import Q
from .utils import geolocator

from .models import Job, JobApplication
from .serializers import JobCreateSerializer, JobSerializer, JobUpdateSerializer, JobApplicationSerializer
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
    jobs = Job.objects.filter(is_open=True, assigned_provider__isnull=True).order_by("-id")  # only open jobs, newest first

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
    jobs = Job.objects.filter(is_open=True, status='open').order_by("-id")

    # Filter by services
    services = request.GET.get("services")
    if services:
        service_ids = services.split(",")
        for service_id in service_ids:
            jobs = jobs.filter(services__id=service_id)

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
    if max_distance:
        user_coord = None

        # use typed location if provided
        location = request.GET.get("location")
        if location:
            geocoded = geolocator.geocode(location)
            if geocoded:
                user_coord = (geocoded.latitude, geocoded.longitude)
                print(f"Using input location: {user_coord}")

        # fall back to profile location
        if user_coord is None and request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            if profile.latitude and profile.longitude:
                user_coord = (profile.latitude, profile.longitude)
                print(f"Using profile coord: {user_coord}")

        if user_coord:
            for job in jobs:
                if job.latitude and job.longitude:
                    dist = haversine(user_coord, (job.latitude, job.longitude), unit=Unit.MILES)
                    print(f"Job {job.id} distance: {dist} miles")
            jobs = [
                job for job in jobs
                if job.latitude and job.longitude and
                haversine(user_coord, (job.latitude, job.longitude), unit=Unit.MILES) <= float(max_distance)
            ]
            print(f"Jobs after distance filter: {len(jobs)}")
        else:
            print("No user_coord found, skipping distance filter")

    serializer = JobSerializer(jobs, many=True, context={"request": request})
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_applications(request):
    profile = request.user.profile

    if not hasattr(profile, "serviceprovider"):
        raise PermissionDenied("You are not a service provider")

    provider = profile.serviceprovider

    apps = JobApplication.objects.filter(provider=provider)

    serializer = JobApplicationSerializer(apps, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def apply_to_job(request, job_id):
    profile = request.user.profile

    if not hasattr(profile, "serviceprovider"):
        raise PermissionDenied("You are not a service provider")

    provider = profile.serviceprovider

    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        raise NotFound("Job not found")

    if job.assigned_provider is not None or job.status != "open":
        return Response(
            {"detail": "This job is no longer accepting applications"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if JobApplication.objects.filter(job=job, provider=provider).exists():
        return Response(
            {"detail": "You have already applied to this job"},
            status=status.HTTP_400_BAD_REQUEST
        )


    application = JobApplication.objects.create(
        job=job,
        provider=provider,
    )

    return Response(
        {"detail": "Application submitted", "application_id": application.id},
        status=status.HTTP_201_CREATED
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def accept_application(request, application_id):
    profile = request.user.profile

    job_application = JobApplication.objects.select_related("job", "provider").filter(id=application_id).first()

    if not job_application:
        raise NotFound("Application not found")

    job = job_application.job

    if job.customer != profile:
        raise PermissionDenied("You do not own this job")

    if job.assigned_provider is not None or job.status != "open":
        return Response(
            {"detail": "Job is no longer available"},
            status=status.HTTP_400_BAD_REQUEST
        )

    provider = job_application.provider

    job.assigned_provider = provider
    job.status = "in_progress"
    job.save()

    job_application.status = "accepted"
    job_application.save()

    JobApplication.objects.filter(job=job).exclude(id=job_application.id).update(
        status="rejected"
    )

    return Response(
        {"detail": "Application accepted and provider assigned"},
        status=status.HTTP_200_OK
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def complete_job(request, job_id):
    profile = request.user.profile

    if not hasattr(profile, "serviceprovider"):
        raise PermissionDenied("You are not a service provider")

    provider = profile.serviceprovider

    job = Job.objects.filter(id=job_id).select_related("assigned_provider").first()
    if not job:
        raise NotFound("Job not found")

    if job.assigned_provider != provider:
        raise PermissionDenied("You are not assigned to this job")

    if job.status != "in_progress":
        return Response(
            {"detail": "Job is not in progress"},
            status=status.HTTP_400_BAD_REQUEST
        )

    job.status = "complete"
    job.is_open = False
    job.save()

    return Response(
        {"detail": "Job marked as complete"},
        status=status.HTTP_200_OK
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_assigned_jobs(request):
    profile = request.user.profile

    if not hasattr(profile, "serviceprovider"):
        raise PermissionDenied("You are not a service provider")

    provider = profile.serviceprovider

    jobs = Job.objects.filter(
        assigned_provider=provider
    ).order_by("-created_at")
    serializer = JobSerializer(jobs, many=True, context={"request": request})
    return Response(serializer.data)