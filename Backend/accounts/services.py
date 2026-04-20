from .models import ServiceProvider

def approve_application(application):
    profile = application.profile

    # 1. update profile
    profile.role = "provider"
    profile.save()

    # 2. create provider
    provider, created = ServiceProvider.objects.get_or_create(
        profile=profile
    )

    # 3. assign services
    provider.services.set(application.skills)

    # 4. mark application
    application.status = "approved"
    application.save()