from django.shortcuts import render
from django.http import JsonResponse
from api.models import Uri_link

def index(request, g_link):
    try:
        url_db = Uri_link.objects.get(url=g_link)
        return render(request, 'webcam_cap/index.html', {'name':url_db.name })
    except Uri_link.DoesNotExist:
        return JsonResponse({"status":"link not found"}, status=404)
