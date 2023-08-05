from .views import CredentialsView
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

router.register(r"", CredentialsView, "Credentials")

urlpatterns = router.urls
