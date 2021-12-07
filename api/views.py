from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from os.path import isfile, isdir
from os import mkdir, listdir

from base64 import b64decode, b64encode
from loguru import logger
from datetime import datetime as dt
from .models import Uri_link
from shutil import rmtree

def id_maker(p_link,id,date):
    f_path = f"media/{p_link}/{date}_{id}.png"
    logger.info(f"{f_path} started!")
    while isfile(f_path):
        id += 1
        f_path = f"media/{p_link}/{date}_{id}.png"
        logger.debug(f"{f_path=}")
    return f_path
    """
    f_path = f"media/{p_link}/{date}_{id}.png"
    if isfile(f_path):
        logger.debug(f"file with {id=} already exists, making new")
        id += 1
        id = id_maker(p_link=p_link,id=id, date=date)
        #change f_path?
    else:
        logger.info(f"file with {id=} not exists, return ")
        return id
    """


logger.add("logs.json", format="{time} {level} {message}", level="DEBUG", rotation="5 MB", compression="zip", serialize=True)
@api_view(['POST'])
def pic_saver(request, p_link):
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
        if ip != url_db.ip:
            logger.info(f"New {ip=} made a post request to {p_link}, saved!")
            url_db.ip = ip
            url_db.save()
        else:
            logger.debug(f"Old {ip=} made a post request to {p_link}...")
    except Exception as e:
        logger.error(f"Error during writing {ip=} to DB, reason: {e}")

    try:
        data = JSONParser().parse(request)
        b64_e = data['b64_pic'].split(',')[1]
        decoded = b64decode(b64_e)

        date = dt.now().strftime("%d_%m_%Y")
        
        gf_path = id_maker(p_link=p_link, id=0,date=date)
        logger.debug(f"{gf_path=}")
        with open(gf_path, "wb") as f:
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
        return JsonResponse({"ips":url_db.get_ips, "photo_ip":None,"photos":None},status=200)
    except Exception as e:
        return JsonResponse({"error":e},status=400)
    return JsonResponse({"ips":url_db.get_ips, "photo_ip":url_db.ip, "photos":photo_arr},status=200)

@api_view(["DELETE"])
def del_log(request, link):
    try:
        url_db = Uri_link.objects.get(url=link).delete()
        rmtree(f"media/{link}")
    except Uri_link.DoesNotExist:
        return JsonResponse({"status":"Not found"}, status=404)
    except Exception as e:
        return JsonResponse({"status":"something gone wrong"}, status=400)
    return JsonResponse({"status":"Deleted"}, status=200)
 
