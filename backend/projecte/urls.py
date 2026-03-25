"""
URL configuration for projecte project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path ,include
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static



@csrf_exempt
def query_api(request, q_name):
    if request.method == "GET":
        from hex.users.infra import q_bus
        try:
            q_json = request.GET.dict()
            query_class = q_bus.get_query_class(q_name)
            q = query_class(**q_json)
            res = q_bus.dispatch(q)
            result = [e.to_primitive() for e in res] if type(res)==list else res.to_primitive()
            return JsonResponse(result, safe=False)
        except:
            import traceback; traceback.print_exc()
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def command_api(request, c_name):
    if request.method == "POST":
        import json
        from hex.users.infra import c_bus
        from hex.users.domain.exceptions import UsernameAlreadyExists
        from hex.users.domain.exceptions import EmailAlreadyExists
        from hex.users.domain.exceptions import DNIAlreadyExists
        try:
            c_json = json.loads(request.body)
            command_class = c_bus.get_command_class(c_name)
            cmd = command_class(**c_json)
            c_bus.dispatch(cmd)

            return JsonResponse({"status": "ok"})
        except UsernameAlreadyExists:
            return JsonResponse( {'detail':"Username already exists"},status=400,safe=False)
        except EmailAlreadyExists:
            return JsonResponse( {'detail':"Email already exists"},status=400,safe=False)
        except DNIAlreadyExists:
            return JsonResponse( {'detail':"DNI already exists"},status=400,safe=False)
    return JsonResponse({"error": "Method not allowed"}, status=405)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('query/<str:q_name>/', query_api, name='query_api'),
    path('command/<str:c_name>/', command_api, name='command_api'),
    path("mailing/", include("mailing.urls")),
    path('summernote/', include('django_summernote.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

