from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .forms import AddMessageForm, ReadMessageForm
from .models import Message, Attachment
from chats.models import Member


@csrf_exempt
@login_required
@require_http_methods(['POST'])
def add_message(request):
    form = AddMessageForm(request.user, request.POST, request.FILES)
    if form.is_valid():
        message = form.save()
        return JsonResponse({'response': {'message': message['message'].to_json(),
                                          'attachment': message['attachment'].to_json()}})
    return JsonResponse({'error': form.errors}, status=400)


@csrf_exempt
@login_required
@require_http_methods(['POST'])
def read_message(request):
    form = ReadMessageForm(request.user, request.POST)
    if form.is_valid():
        reader = form.save()
        return JsonResponse({'response': reader.to_json()})
    return JsonResponse({'error': form.errors}, status=400)


@login_required
@require_http_methods(['GET'])
def get_list_messages(request):
    chat_id = request.GET.get('chat')
    if chat_id is None or not chat_id.isdigit():
        return JsonResponse({'response': []}, status=400)
    user_id = request.user.id

    member = Member.objects.select_related('chat', 'user').filter(chat=chat_id, user=user_id)
    if member:
        message_list = Message.objects.select_related('chat').filter(chat=chat_id)
        attachment_list = Attachment.objects.select_related('chat').filter(chat=chat_id)
        return JsonResponse({'response': {'current_user_id': user_id, 'messages_list':
                            [{'message': message.to_json(), 'attachment': attachment.to_json()}
                                for message, attachment in zip(message_list, attachment_list)]}})
    else:
        return JsonResponse({'response': []}, status=400)