import datetime
import json
import random
import itertools
import re

from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from .models import *


def getDays(index):
    if index == 0: return 1
    if index == 1: return 2
    if index == 2: return 4
    return 4

@csrf_exempt
def words(request):


    if request.method == "POST":

        result = json.loads(request.POST['result'])

        for key, value in result.items():

            word = Word.objects.get(id=int(key))
            print(key, value)

            word.errors += int(value)
            word.totalRepeatedTimes +=1

            if int(value) != 0:
                word.repeatDate = datetime.date.today() + datetime.timedelta(days=1)
                word.repeatIndex = 0
            else:
                word.repeatIndex = word.repeatIndex + 1
                word.repeatDate = datetime.date.today() + datetime.timedelta(days=getDays(word.repeatIndex))

            word.save()
        return redirect("words")




    storages = WordStorage.objects.all()
    wordsToAdd  = list()

    for storage in storages:

        if storage.initialData == "": continue

        for l in storage.initialData.split("\n"):
            if l == "": continue

            ls = l.split(",")
            for w in ls:

                if storage.storageName == "пре,при":
                    if "пре" in w:
                        w = w.replace("пре", "прЕ", 1)
                    elif "при" in w:
                        w = w.replace("при", "прИ", 1)

                wordsToAdd.append((w, storage))

        storage.initialData = ""
        storage.save()


    print(wordsToAdd)
    for w2a in wordsToAdd:

        word = Word()

        word.word = w2a[0]
        word.storage = w2a[1]
        word.repeatDate = datetime.date.today()

        word.save()

    del wordsToAdd


    wordsResult = []
    words = list(Word.objects.filter(repeatDate__lte=datetime.date.today()).order_by('-repeatIndex'))


    words2 = []

    for word in words:
        if word.word.replace(" ", "").replace("\n", "").replace("\r", "") == "": continue
        if not word.storage.enabled: continue
        words2.append(word)

    words = words2

    random.shuffle(words)
    words = words[:25]

    for word in words:

        renderWord = word.word.replace("1", "?").replace("0", "?")

        renderWord = re.sub(r"[АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЭЮЯЪЬ]{2,}", "?", renderWord)
        renderWord = re.sub(r"[АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЭЮЯЪЬ]+", "?", renderWord)

        right_answer = FormRightAnswer(word.word)


        wordRightImposter = word.word.replace("0", "").replace("1", " ")


        wordsResult.append({
            "renderWord": renderWord.replace("\r", "").replace("\n", "").replace(";", ""),
            "rightAnswer": right_answer.lower().replace("\r", "").replace("\n", "").replace(";", ""),
            "wordId": word.id,
            "wordRightImposter": wordRightImposter.replace("\r", "").replace("\n", "").replace(";", "")
        })


    # form pairs
    copied = []

    for word in wordsResult:
        realWord = Word.objects.get(id=word['wordId'])
        if realWord.storage.ignore2ndStage: continue

        copied.append(word)

    stage2tasks = []
    cache = {}

    for comb in itertools.combinations(copied, r=4):

        for i in range(len(comb)):
            w = comb[i]
            if len(w['rightAnswer']) == 1 or w['rightAnswer'] == "нн": continue

            word = Word.objects.get(id=int(w['wordId']))

            indexes = []
            combglist = list(comb)

            for j in range(len(word.word)):
                c = word.word[j]
                if c.isupper(): indexes.append((j, c))

            for index in indexes:
                lw = word.word.lower()

                forRenderCopy = list(lw)
                forRenderCopy[index[0]] = "?"

                newWord = w.copy()
                newWord['renderWord'] = "".join(forRenderCopy).replace("\r", "").replace("\n", "").replace(";", "")
                newWord['rightAnswer'] = index[1].lower().replace("\r", "").replace("\n", "").replace(";", "")

                combglist[i] = newWord
                if not TryCombination(tuple(combglist)): continue
                comb = tuple(combglist)

                break
            break

        if not TryCombination(comb): continue

        doContinue = False
        for c in comb:
            if c['wordId'] in cache:
                doContinue = True
                break

        if doContinue: continue

        for c in comb:
            cache[c['wordId']] = c

        stage2tasks.append([c for c in comb])

    for comb in itertools.combinations(copied, r=4):

        incache = set()

        for c in comb:
            incache.add(c['wordId'] in cache)

        if len(incache) == 1 and list(incache)[0]: continue

        for i in range(len(comb)):
            w = comb[i]
            if len(w['rightAnswer']) == 1 or w['rightAnswer'] == "нн": continue

            word = Word.objects.get(id=int(w['wordId']))

            indexes = []
            combglist = list(comb)

            for j in range(len(word.word)):
                c = word.word[j]
                if c.isupper(): indexes.append((j, c))

            for index in indexes:
                lw = word.word.lower()

                forRenderCopy = list(lw)
                forRenderCopy[index[0]] = "?"

                newWord = w.copy()
                newWord['renderWord'] = "".join(forRenderCopy).replace("\r", "").replace("\n", "").replace(";", "")
                newWord['rightAnswer'] = index[1].lower().replace("\r", "").replace("\n", "").replace(";", "")

                combglist[i] = newWord
                if not TryCombination(tuple(combglist)): continue
                comb = tuple(combglist)

                break
            break

        if not TryCombination(comb): continue

        for c in comb:
            cache[c['wordId']] = c

        stage2tasks.append([c for c in comb])
    #
    # for comb in itertools.combinations(copied, r=4):
    #     answers = set()
    #     incache = set()
    #     answersList = list()
    #
    #     for c in comb:
    #         incache.add(c['wordId'] in cache)
    #         answers.add(c['rightAnswer'])
    #         answersList.append(c['rightAnswer'])
    #
    #     if len(incache) == 1 and list(incache)[0]: continue
    #
    #     setasglist = list(answers)
    #     if len(answers) != 2 or answersList.count(setasglist[0]) == answersList.count(setasglist[1]): continue
    #
    #     for c in comb:
    #         cache[c['wordId']] = c
    #
    #     stage2tasks.append([c for c in comb])

    #print(stage2tasks)
    #print(len(stage2tasks))
    print(len(cache))

    return render(request, 'wordsTemplate.html', {
        'wordsJson': json.dumps(wordsResult, ensure_ascii=False),
        'stage2Json' : json.dumps(stage2tasks, ensure_ascii=False)
    })

def TryCombination(comb : tuple):
    answers = set()
    answersList = list()

    for c in comb:
        answers.add(c['rightAnswer'])
        answersList.append(c['rightAnswer'])

    setasglist = list(answers)
    if ('а' in answers and 'о' not in answers) \
        or ('о' in answers and 'а' not in answers) \
        or ('е' in answers and 'и' not in answers) \
        or ('и' in answers and 'е' not in answers) \
        or ('н' in answers and 'нн' not in answers) \
        or ('нн' in answers and 'н' not in answers) \
        or (' ' in answers and '' not in answers) \
        or ('' in answers and ' ' not in answers) \
        or len(answers) != 2 or answersList.count(setasglist[0]) == answersList.count(setasglist[1]): return False

    return True

def FormRightAnswer(word: str):
    right_answer = ""
    for c in word:
        if c == "0":
            right_answer += ""
        elif c == "1":
            right_answer += " "
        elif c in "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЭЮЯЪЬ":
            right_answer += c

    return right_answer
