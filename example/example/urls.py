from crudbuilder import urls
from django.contrib import admin
from django.db import connection
from django.urls import include, re_path

tables = connection.introspection.table_names()

urlpatterns = [
    # Examples:
    # re_path(r'^$', 'example.views.home', name='home'),
    # re_path(r'^blog/', include('blog.urls')),
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^auth/", include("django.contrib.auth.urls")),
    re_path(r"^crud/", include(urls)),
]

if "django_content_type" in tables:
    from example.views import MyCustomPersonCreateView, MyCustomPersonListView

    urlpatterns += [
        re_path(
            r"^mycustom_people/$",
            MyCustomPersonListView.as_view(),
            name="mycustom-people",
        ),
        re_path(
            r"^mycustom_people/create/$",
            MyCustomPersonCreateView.as_view(),
            name="mycustom-create",
        ),
    ]
