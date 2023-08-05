"""API URLs, called by Views, used for add/edit actions."""
__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2022, Andrea Dainese"
__license__ = "GPLv3"
__date__ = "2022-09-07"
__version__ = "0.9.25"

from netbox.api.routers import NetBoxRouter
from netdoc.api import views


app_name = "nedoc"  # pylint: disable=invalid-name

router = NetBoxRouter()
router.register("credential", views.CredentialViewSet)
router.register("diagram", views.DiagramViewSet)
router.register("discoverylog", views.DiscoveryLogViewSet)
router.register("discoverable", views.DiscoverableViewSet)

urlpatterns = router.urls
