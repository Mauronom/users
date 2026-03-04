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
from django.urls import path
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def query_api(request, q_name):
    print(request.method)
    if request.method == "GET":
        from hex.users.infra import q_bus
        try:
            result = [e.to_primitive() for e in q_bus.dispatch(q_name)]
            print(result)
            return JsonResponse(result, safe=False)
        except:
            import traceback; traceback.print_exc()
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def query_api_with_param(request, q_name, param):
    if request.method == "GET":
        from hex.users.infra import q_bus
        try:
            result = q_bus.dispatch(q_name, param)
            if result is None:
                return JsonResponse({"error": "Not found"}, status=404)
            return JsonResponse(result.to_primitive(), safe=False)
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
            body = request.body.decode("utf-8")
            c_info = json.loads(body) if body else {}

            c_bus.dispatch(c_name, c_info)

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
    path('query/<str:q_name>/<str:param>/', query_api_with_param, name='query_api_with_param'),
    path('query/<str:q_name>/', query_api, name='query_api'),
    path('command/<str:c_name>/', command_api, name='command_api'),
]

