from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import ServiceProvider, Profile
from .models import Review, ReviewImage
from .serializers import ReviewSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_review(request, service_provider_id):
    try:
        profile = Profile.objects.get(user=request.user)
        service_provider = ServiceProvider.objects.get(id=service_provider_id)

        if service_provider.profile.user == request.user:
            return Response({"error": "Cannot review yourself"}, status=400)
    except (Profile.DoesNotExist, ServiceProvider.DoesNotExist):
        return Response({"error": "Invalid user or service provider"}, status=404)

    data = request.data.copy()
    data["service_provider_id"] = service_provider.id

    serializer = ReviewSerializer(data=data, context={"request": request})
    if serializer.is_valid():
        review = serializer.save()

        images = request.FILES.getlist("images")
        for img in images:
            ReviewImage.objects.create(review=review, image=img)

        return Response(ReviewSerializer(review, context={"request": request}).data, status=201)

    return Response(serializer.errors, status=400)


@api_view(["GET"])
def get_reviews(request, service_provider_id):
    reviews = Review.objects.filter(service_provider_id=service_provider_id).order_by("-created_at")
    serializer = ReviewSerializer(reviews, many=True, context={"request": request})
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_review(request, review_id):
    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        return Response({"error": "Review not found"}, status=404)

    if review.reviewer.user != request.user:
        return Response({"error": "Not allowed"}, status=403)

    review.delete()
    return Response(status=204)


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_review(request, review_id):
    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        return Response({"error": "Review not found"}, status=404)

    if review.reviewer.user != request.user:
        return Response({"error": "Not allowed"}, status=403)

    data = request.data.copy()
    data.pop("service_provider_id", None)
    data.pop("job_id", None)
    data.pop("reviewer", None)
    data.pop("service_provider", None)
    data.pop("job", None)

    serializer = ReviewSerializer(
        review,
        data=data,
        partial=True,
        context={"request": request}
    )

    if serializer.is_valid():
        updated_review = serializer.save()

        for img in request.FILES.getlist("images"):
            ReviewImage.objects.create(review=updated_review, image=img)

        return Response(ReviewSerializer(updated_review, context={"request": request}).data)

    return Response(serializer.errors, status=400)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_review_image(request, image_id):
    try:
        image = ReviewImage.objects.get(id=image_id)
    except ReviewImage.DoesNotExist:
        return Response({"error": "Image not found"}, status=404)

    if image.review.reviewer.user != request.user:
        return Response({"error": "Not allowed"}, status=403)

    image.delete()
    return Response(status=204)