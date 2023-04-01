from datetime import datetime, date
import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from .models import *


@csrf_exempt
def words(request):


    storages = WordStorage.objects.all()
    wordsToAdd  = list()

    for storage in storages:

        if storage.initialData == "": continue

        for l in storage.initialData.split("\n"):
            if l == "": continue

            ls = l.split(",")
            for w in ls:
                wordsToAdd.append((w, storage))

        storage.initialData = ""
        storage.save()

    for w2a in wordsToAdd:

        word = Word()

        word.word = w2a[0]
        word.storage = w2a[1]
        word.repeatDate = datetime.now()

        word.save()

    del wordsToAdd


    wordsResult = []
    words = Word.objects.filter(repeatDate__lte=date.today())

    for word in words:

        renderWord = word.word \
            .replace("1", "?") \
            .replace("0", "?") \
            .replace("А", "?") \
            .replace("Я", "?") \
            .replace("Ю", "?") \
            .replace("У", "?") \
            .replace("Е", "?") \
            .replace("И", "?") \
            .replace("О", "?") \
            .replace("Н", "?") \

        right_answer = ""
        for c in word.word:
            if c == "0":
                right_answer += ""
            elif c == "1":
                right_answer += " "
            elif c == "Н":
                right_answer += c
            elif c == "А":
                right_answer += c
            elif c == "О":
                right_answer += c
            elif c == "Е":
                right_answer += c
            elif c == "И":
                right_answer += c
            elif c == "У":
                right_answer += c
            elif c == "Ю":
                right_answer += c



        wordImposter = ""

        for i in range(len(word.word)):
            c = word.word[i]
            if c == "0":
                wordImposter += " "
            elif c == "1":
                wordImposter += ""
            elif c == "Н" and i + 1 != len(word.word) and  word.word[i + 1] == "Н":
                wordImposter += ""
            elif c == "Н" and i - 1 >= 0 and word.word[i - 1] == "Н":
                wordImposter += "Н"
            elif c == "Н":
                wordImposter += "НН"
            elif c == "А":
                wordImposter += "О"
            elif c == "О":
                wordImposter += "А"
            elif c == "Е":
                wordImposter += "И"
            elif c == "И":
                wordImposter += "Е"
            elif c == "У":
                wordImposter += "Ю"
            elif c == "Ю":
                wordImposter += "У"
            else:
                wordImposter += c


        wordRightImposter = word.word.replace("0", "").replace("1", " ")

        wordsResult.append({
            "renderWord": renderWord.replace("\r", "").replace("\n", "").replace(";", ""),
            "rightAnswer": right_answer.lower().replace("\r", "").replace("\n", "").replace(";", ""),
            "wordId": word.id,
            "wordImposter": wordImposter.replace("\r", "").replace("\n", "").replace(";", ""),
            "wordRightImposter": wordRightImposter.replace("\r", "").replace("\n", "").replace(";", "")
        })

    return render(request, 'wordsTemplate.html', {'wordsJson': json.dumps(wordsResult, ensure_ascii=False)})
