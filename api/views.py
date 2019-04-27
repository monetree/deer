from django.shortcuts import render
from django.http import JsonResponse
import pymongo
from bson.json_util import dumps
import json
import math

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["game"]

mycol = mydb["test_collection"]


def users(request):
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    country = request.GET.get('country')

    if limit is None:
        limit = 10
    else:
        limit = int(limit)

    if page:
        page = int(page)
        index = int(limit) * int(page - 1)
    else:
        index = 0

    api = {
        "limit": limit,
        "page": page,
        "total_pages": math.ceil(mycol.find().count() / limit),
        "has_more": None,
        "data" : []
    }
    if country:
        query = {"country": country}
    else:
        query = {}
    data = mycol.find(query).skip(index).limit(limit)
    res = json.loads(dumps(data))

    # check has more
    has = mycol.find(query).skip(index + 1).limit(limit)
    more = json.loads(dumps(has))
    if len(more) > 0:
        api['has_more'] = True
    else:
        api['has_more'] = False

    api['data'] = res
    return JsonResponse(api)
