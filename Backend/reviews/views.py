from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Review
from accounts.models import ServiceProvider
from .serializers import ReviewSerializer
from accounts.models import Profile


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
    data["service_provider"] = service_provider.id

    serializer = ReviewSerializer(data=data)
    if serializer.is_valid():
        serializer.save(reviewer=profile)
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
        print(review.reviewer.user.id, request.user.id)
        return Response({"error": "Not allowed"}, status=403)

    review.delete()
    return Response({"message": "Review deleted"}, status=204)