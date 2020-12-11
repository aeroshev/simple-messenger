from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import User


@login_required
@require_http_methods(['GET'])
def get_profile(request):
    user = get_object_or_404(User, username=request.user.username)
    return JsonResponse(user.to_json())


@login_required
@require_http_methods(['GET'])
def search(request):
    first_name = request.GET.get('first_name')
    last_name = request.GET.get('last_name')
    if first_name is None or last_name is None:
        return JsonResponse({'response': []}, status=400)

    users = User.objects.filter(first_name__icontains=first_name, last_name__icontains=last_name)
    return JsonResponse({'response': [user.to_json() for user in users]})
