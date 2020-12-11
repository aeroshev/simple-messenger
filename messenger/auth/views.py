from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return render(request, 'registration/home.html')
