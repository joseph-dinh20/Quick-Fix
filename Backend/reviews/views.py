from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Review, ReviewImage
from accounts.models import ServiceProvider
from .serializers import ReviewSerializer
from accounts.models import Profile
from django.db.models import Avg


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_review(request, service_provider_id):
    print(request.data, service_provider_id)
    try:
        profile = Profile.objects.get(user=request.user)
        service_provider = ServiceProvider.objects.get(id=service_provider_id)

        if service_provider.profile.user == request.user:
          return Response({"error": "Cannot review yourself"}, status=400)
    except (Profile.DoesNotExist, ServiceProvider.DoesNotExist):
        return Response({"error": "Invalid user or service provider"}, status=404)

    data = request.data.copy()
    data["service_provider"] = service_provider.id

    serializer = ReviewSerializer(data=data)
    if serializer.is_valid():
        review = serializer.save(reviewer=profile)

        provider = review.service_provider
        agg = provider.reviews.aggregate(avg=Avg("rating"))
        provider.average_rating = agg["avg"] or 0
        
        provider.total_rating = provider.reviews.count()
        provider.save()

        images = request.FILES.getlist("images")
        for img in images:
            ReviewImage.objects.create(review=review, image=img)

        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(["GET"])
def get_reviews(request, service_provider_id):
    reviews = Review.objects.filter(service_provider_id=service_provider_id).order_by("-created_at")
    serializer = ReviewSerializer(reviews, many=True)
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

    provider = review.service_provider
    review.delete()

    agg = provider.reviews.aggregate(avg=Avg("rating"))
    avg_rating = agg["avg"] or 0
    total = provider.reviews.count()

    provider.average_rating = avg_rating
    provider.total_rating = total
    provider.save()

    return Response({"message": "Review deleted"}, status=204)


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_review(request, review_id):
    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        return Response({"error": "Review not found"}, status=404)

    if review.reviewer.user != request.user:
        return Response({"error": "Not allowed"}, status=403)

    serializer = ReviewSerializer(review, data=request.data, partial=True)

    if serializer.is_valid():
        review = serializer.save()

        for img in request.FILES.getlist("images"):
            ReviewImage.objects.create(review=review, image=img)

        provider = review.service_provider
        agg = provider.reviews.aggregate(avg=Avg("rating"))
        provider.average_rating = agg["avg"] or 0
        provider.save()

        return Response(ReviewSerializer(review).data)

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
    return Response({"message": "Image deleted"}, status=204)