from datetime import date
import json
import datetime

from django.shortcuts import render

# Create your views here.
from .models import Pronounce
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):


    if request.method == "POST":

        words = json.loads(request.POST['result'])

        for word in words:

            bdWord : Pronounce = Pronounce.objects.get(id=word['id'])
            bdWord.errorsCount += word['errors']
            bdWord.repeatsCount += 1
            if word['errors'] == 0:
                bdWord.repeatDate = date.today() + datetime.timedelta(days=2)
            else:
                bdWord.repeatDate = date.today() + datetime.timedelta(days=1)
            bdWord.save()


    pronounces = Pronounce.objects.filter(repeatDate__lte=date.today())

    resultList = list()

    for pronounce in pronounces:

        resultItem = dict()
        resultItem['id'] = pronounce.id
        resultItem["letters"] = []
        resultItem["errors"] = 0
        resultItem["right"] = pronounce.word
        resultItem["hint"] = ""

        if pronounce.hint != None:
            resultItem["hint"] = pronounce.hint.name

        for s in pronounce.word:
            if s in "АЯУЮЫИОЁЕЭ":
                resultItem["letters"].append({
                    "class": "btn right-letter ml-1 mr-1",
                    "letter": s.lower(),
                    "right": True
                })
            elif s in "аяуюыиёоеэ":
                resultItem["letters"].append({
                    "class": "btn dangeon-letter ml-1 mr-1",
                    "letter": s,
                    "right": False
                })
            else:
                resultItem["letters"].append({
                    "class": "btn fine-letter ml-1 mr-1",
                    "letter": s,
                    "right": False
                })

        resultList.append(resultItem)



    return render(request, "pronounce.html", {"words": json.dumps(resultList, ensure_ascii=False)})