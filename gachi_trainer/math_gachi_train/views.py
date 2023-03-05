import datetime
import random

from django.forms import formset_factory
from django.shortcuts import render
from django.http import HttpResponse
from datetime import date, timedelta
import math
import itertools

# Create your views here.
from .models import *
from .forms import *
from django.views.decorators.csrf import csrf_exempt

MyModelFormSet = formset_factory(TaskForm, extra=0)

@csrf_exempt
def index(request):

    if request.method == "POST":

        print(request.POST)
        fr = MyModelFormSet(request.POST)

        for f in fr:


            if not f.is_valid():
                print(f.data)
                continue
            print(f"form valid: {f.cleaned_data}")
            collection = CollectionModel.objects.get(name=f.cleaned_data['collection'])

            task = None
            if TaskModel.objects.filter(task_name=f.cleaned_data['task_name']).exists():
                task = TaskModel.objects.get(task_name=f.cleaned_data['task_name'])
                task.task_repeat_in_index = task.task_repeat_in_index + 1
            else:
                task = TaskModel()

            task.banned = f.cleaned_data['cost'] == 0
            task.task_cost = f.cleaned_data['cost']
            task.task_name = f.cleaned_data['task_name']
            task.collection = collection
            task.task_repeat_date = date.today() + datetime.timedelta(days=f.cleaned_data['days'])

            task.save()

    maximumCost = 5
    repeat_tasks = []
    are_new = []

    total_repeat_cost = 0
    for collection in CollectionModel.objects.all():

        if not collection.enabled: continue
        # tasks = TaskModel.objects.get(collection=collection)

        cur_tasks = collection.tasks.filter(task_repeat_date__lte=date.today(), banned=False)

        for task in cur_tasks:
            total_repeat_cost += task.task_cost
            task.task_repeat_in_index = task.task_repeat_in_index + 1
            repeat_tasks.append(task)

    print(f"Total tasks to repeat: {len(repeat_tasks)}: {repeat_tasks}")

    result_tasks = []
    if total_repeat_cost == maximumCost:
        result_tasks = repeat_tasks
    elif total_repeat_cost > maximumCost:
        result_tasks = formListOfTasks(maximumCost, repeat_tasks)
        print(f"Added repeat tasks: {len(result_tasks)}: {result_tasks}")
    else:
        for rp in repeat_tasks:
            result_tasks.append(rp)
        print(f"Added repeat tasks: {len(result_tasks)}: {result_tasks}")
        # print(best_combination, best_combination_cost)

    total_result_cost = 0
    for task in result_tasks:
        are_new.append(False)
        total_result_cost += task.task_cost

    if total_result_cost < maximumCost:
        # add random tasks in

        iterators = list()
        imagine_tasks = list()
        collections = list()

        cal = list(CollectionModel.objects.all())
        random.shuffle(cal)

        for collection in cal:

            task_ranges = collection.task_intervals.split(";")
            imagine_tasks_cur_collection = list()

            for i in range(int(len(task_ranges) / 2)):

                r1 = int(task_ranges[i * 2])
                r2 = int(task_ranges[i * 2 + 1])

                for r in range(r1, r2):

                    task_name = f"{collection.short_name}#{r}"


                    if TaskModel.objects.filter(task_name=task_name).exists():
                        continue

                    task_model = TaskModel()
                    task_model.collection = collection
                    task_model.task_cost = collection.avg_cost
                    task_model.task_name = task_name
                    task_model.task_repeat_in_index = 0
                    imagine_tasks_cur_collection.append(task_model)

            imagine_tasks.append(imagine_tasks_cur_collection)
            iterators.append(0)
            collections.append(collection)

        #print(iterators)
        #print(imagine_tasks)
        #print(collections)
        glist = list()

        while len(glist) < 10:
            repeat = False
            #print(iterators)
            for collectionIndex in range(len(collections)):
                sp = iterators[collectionIndex]
                #print(collectionIndex, sp)

                for i in range(sp, sp + collections[collectionIndex].priority):
                    #print(i, imagine_tasks[collectionIndex])
                    if i >= len(imagine_tasks[collectionIndex]):
                        break
                    glist.append(imagine_tasks[collectionIndex][i])
                    repeat = True
                iterators[collectionIndex] = sp + collections[collectionIndex].priority

            if not repeat: break
        #print(f"Glist: {glist}")
        random_tasks = formListOfTasks(maximumCost - total_result_cost, glist)
        print(f"Added random tasks {len(random_tasks)}: {random_tasks}")

        for rt in random_tasks:
            are_new.append(True)
            result_tasks.append(rt)

    total_result_cost = 0
    for task in result_tasks:
        total_result_cost += task.task_cost
    print(f"Total result cost: {total_result_cost}")

    # print(total_combinations)

    # print(list(CollectionModel.objects.all()))

    initial_data = [{'cost': obj.task_cost, 'days': obj.getDays(), 'task_name': obj.task_name, 'collection' : obj.collection.name} for obj in result_tasks]
    formset = MyModelFormSet(initial=initial_data)
    return render(request, 'index.html', {'tasks': result_tasks, 'formset': formset, 'areNew': are_new})


def formListOfTasks(maximumCost: int, repeat_tasks: list):
    best_combination = list()
    best_combination_cost = 0

    for combination in itertools.combinations(repeat_tasks, r=len(repeat_tasks)):

        for sp in range(len(repeat_tasks)):

            total_iterations = 0
            i = sp
            curcost = 0
            cur_comb = list()
            while curcost < maximumCost and total_iterations < len(repeat_tasks):

                if curcost + combination[i].task_cost > maximumCost:
                    break
                curcost += combination[i].task_cost
                cur_comb.append(combination[i])
                i += 1
                total_iterations += 1
                if i == len(repeat_tasks):
                    i = 0

            if best_combination_cost < curcost:
                best_combination_cost = curcost
                best_combination = cur_comb

    #print(best_combination, best_combination_cost)
    return best_combination
