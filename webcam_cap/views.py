from django.shortcuts import render
from django.http import JsonResponse
from api.models import Uri_link

def index(request, g_link):
    try:
        url_db = Uri_link.objects.get(url=g_link)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        if ip not in url_db.get_ips:
            url_db.get_ips.append(ip)
            url_db.save()
        return render(request, 'webcam_cap/index.html', {'name':url_db.name })
    except Uri_link.DoesNotExist:
        return JsonResponse({"status":"link not found"}, status=404)
