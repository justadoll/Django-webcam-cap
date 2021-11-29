from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from base64 import b64decode
from loguru import logger
from datetime import datetime as dt
from os.path import isfile

logger.add("logs.json", format="{time} {level} {message}", level="DEBUG", rotation="5 MB", compression="zip", serialize=True)
@api_view(['POST'])
def pic_saver(request):
    logger.debug(request)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    logger.info(f"{ip=}")
    try:
        data = JSONParser().parse(request)
        b64_e = data['b64_pic'].split(',')[1]
        decoded = b64decode(b64_e)

        date = dt.now().strftime("%d_%m_%Y")
        tmp = 0
        f_path = f"media/{date}_{ip}_{tmp}.png"
        if isfile(f_path):
            tmp += 1
        with open(f"media/{date}_{ip}_{tmp}.png","wb") as f:
            f.write(decoded)
        return JsonResponse({"status":"saved"}, status=200)
    except Exception as e:
        logger.error(e)
        return JsonResponse({"status":"error"}, status=400)
