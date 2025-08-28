import pytest
from django.urls import path
from django.http import HttpResponse
from django.test import override_settings

from coresite.models import Tool


def dummy_tool_detail(request, slug):
    return HttpResponse("ok")


urlpatterns = [path("tools/<slug:slug>/", dummy_tool_detail, name="tool_detail")]


@pytest.mark.django_db
def test_tool_slug_autogenerates_and_uniquifies():
    t1 = Tool.objects.create(title="My Tool")
    t2 = Tool.objects.create(title="My Tool")
    assert t1.slug == "my-tool"
    assert t2.slug == "my-tool-1"


@override_settings(ROOT_URLCONF=__name__)
@pytest.mark.django_db
def test_tool_get_absolute_url_uses_slug():
    tool = Tool.objects.create(title="Example Tool")
    assert tool.get_absolute_url() == f"/tools/{tool.slug}/"


@pytest.mark.django_db
def test_tool_published_manager_filters_correctly():
    published = Tool.objects.create(title="Published", is_published=True)
    Tool.objects.create(title="Draft", is_published=False)
    assert list(Tool.objects.published()) == [published]
