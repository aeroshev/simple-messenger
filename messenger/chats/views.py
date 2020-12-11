from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .forms import ChatForm
from .models import Member


@login_required
@require_http_methods(['GET'])
def chat_list(request):
    consists_in_chats = Member.objects.select_related('user').filter(user=request.user.id)
    return JsonResponse({'response': [user.chat.to_json() for user in consists_in_chats]})


@csrf_exempt
@login_required
@require_http_methods(['POST'])
def create_chat(request):
    form = ChatForm(request.user, request.POST, request.FILES)
    if form.is_valid():
        chat = form.save()
        return JsonResponse({'response': chat.to_json()})
    return JsonResponse({'error': form.errors}, status=400)
