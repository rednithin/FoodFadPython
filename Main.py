import os
import copy
import json
import time
import numpy as np
import matplotlib.pyplot as plt


def Swap(arr, position1, position2):
    temp = arr[position1]
    arr[position1] = arr[position2]
    arr[position2] = temp


def IsTagPresent(foodItem, mytag):
    for tag in foodItem["Tags"]:
        if mytag == tag:
            return True


def IsIngredientPresent(foodItem, allergy):
    for ingredient in foodItem["MajorIngredients"] + foodItem["MinorIngredients"]:
        if ingredient == allergy:
            return True


def RemoveNegativeItems(foodItems, negativeTags):
    length = len(foodItems)

    i = 0
    while i != length:
        for negativeTag in negativeTags:
            if IsTagPresent(foodItems[i], negativeTag):
                length -= 1
                i -= 1
                del foodItems[i]
                break
        i += 1


def RemoveAllergicItems(foodItems, allergies):
    length = len(foodItems)

    i = 0
    while i != length:
        for allergy in allergies:
            if IsIngredientPresent(foodItems[i], allergy):
                length -= 1
                i -= 1
                del foodItems[i]
                break
        i += 1


def PrioritizePositiveItems(foodItems, positiveTags):
    length = len(foodItems)

    i = 0
    partitionIndex = 0
    while i != length:
        for positiveTag in positiveTags:
            if IsTagPresent(foodItems[i], positiveTag):
                Swap(foodItems, partitionIndex, i)
                partitionIndex += 1
        i += 1

    return partitionIndex

def PrioritizePostiveItemsI(foodItems, positiveTags):
    for i in range(1, len(foodItems)):
        j = i - 1
        key = foodItems[i]

        isPositive = False
        for positiveTag in positiveTags:
            if IsTagPresent(foodItems[j], positiveTag):
                isPositive = True
                break

        while j >= 0 and not isPositive:
            foodItems[j+1] = foodItems[j]
            j -= 1
            isPositive = False
            for positiveTag in positiveTags:
                if IsTagPresent(foodItems[j], positiveTag):
                    isPositive = True
                    break

        foodItems[j+1] = key

def GetApplicableFoods(foodItems, negativeTags = [], positiveTags =[], allergies=[]):
    RemoveNegativeItems(foodItems, negativeTags)
    RemoveAllergicItems(foodItems, allergies)
    return PrioritizePositiveItems(foodItems, positiveTags)


def RateIngredients(myIngredients, foodItem, like):
    if like:
        step = 1
    else:
        step = -.75
    for ingredient in foodItem['MajorIngredients']:
        myIngredients.setdefault(ingredient, 0)
        myIngredients[ingredient] += step


def RateFoodItems(ingredients, foodItems):
    for i in range(len(foodItems)):
        foodItems[i]["Rating"] = 0
        for j in foodItems[i]["MajorIngredients"]:
            for ingredient in ingredients.keys():
                if ingredient == j:
                    foodItems[i]["Rating"] += ingredients[ingredient]


def SelectionSort(foodItems):
    for i in range(0,len(foodItems)):
        for j in range(i+1, len(foodItems)):
            if foodItems[j]["Rating"] > foodItems[i]["Rating"]:
                temp = foodItems[i]
                foodItems[i] = foodItems[j]
                foodItems[j] = temp


def DisplayInOrder(foodItems):
    print("Food Items : "*10)
    for i in range(len(foodItems)):
        print(foodItems[i]["Name"] + " : " + str(foodItems[i]["Rating"]))


def PlotIngredientGraph(dictionary):
    x = np.array(list(range(len(dictionary.keys()))))
    y = np.array(list(dictionary.values()))

    plt.plot(x, y, 'r')
    plt.xticks(x, dictionary.keys(), rotation='vertical')
    plt.xlabel('Ingredients')
    plt.ylabel('Frequency')
    plt.show()
    plt.close()
    plt.clf()


def PlotSetGraph(dictionary):
    x = []
    y = []
    for i in dictionary:
        x.append(i['Name'])
        y.append(i['Rating'])

    plt.plot(np.arange(0, len(x)), np.array(y), 'r')
    plt.xticks(np.arange(0, len(x)), x, rotation='vertical')
    plt.xlabel('Food Items')
    plt.ylabel('Taste Parameter')
    plt.show()
    plt.close()
    plt.clf()


def Demonstrate(applicableSet, ingredients, foodItem, like):
    RateIngredients(ingredients, foodItem, like)
    RateFoodItems(ingredients, applicableSet)
    SelectionSort(applicableSet)
    #PrioritizePostiveItemsI(applicableSet, positiveTags)
    #DisplayInOrder(applicableSet)
    PlotIngredientGraph(ingredients)
    PlotSetGraph(applicableSet)


class Item(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)


os.chdir('/home/nithin/Desktop/')
file = open('UniversalSet.txt')
content = file.read()

obj = Item(content)

universalSet = obj.FoodItems
applicableSet = copy.deepcopy(universalSet)


print("Enter name?")
name = input()
print("Enter positive tags?")
positiveTags = input().split(',')
print("Enter negative tags?")
negativeTags = input().split(',')
print("Enter allergies?")
allergies = input().split(',')


GetApplicableFoods(applicableSet, negativeTags, positiveTags, allergies)
ingredients = {}

print("Manual(0) or Automate(1) it? ")
choice = int(input())
if choice == 0:
    while True:
        randomIndices = np.random.randint(0, high=len(applicableSet), size=5)
        randomList = [applicableSet[i] for i in randomIndices]
        randomSet = []
        for randomElement in randomList:
            randomSet.append(randomElement["Name"])
        print(randomSet)
        print('Enter Name Of A Dish : ')
        name = input()
        print('Did you like it?(yes/no)')
        if 'yes' == input():
            like = True
        else:
            like = False

        for i in randomList:
            if i["Name"] == name:
                Demonstrate(applicableSet, ingredients, i, like)

elif choice == 1:
    while True:
        Demonstrate(applicableSet, ingredients, applicableSet[np.random.randint(0, len(applicableSet), size=1)[0]], True)


