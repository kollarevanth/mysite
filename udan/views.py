from django.shortcuts import render
from django.shortcuts import render
from requests import Response
from rest_framework.compat import authenticate
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView,ListAPIView,UpdateAPIView
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# Create your views here.

def process(dir,row,info):
    fp=open(os.path.join(dir, row+'.txt'), 'w')
    li=[1 for i in range(info['numberOfSeats'])]
    c=0
    for i in li:
        if(c in info['aisleSeats']):
            li[c]+=1
        c+=1
    li=[str(i) for i in li]
    temp=",".join(li)
    fp.write(temp)






import os
@api_view(["POST"])
def getScreenDetails(request):
    dir=request.data.get("name")
    os.mkdir(dir)
    seatInfo=dict(request.data.get("seatInfo"))
    print(seatInfo)
    for (k,v) in seatInfo.items():
        process(dir,k,v)

def doReservation(dir,row,seats):
    fp1 = open(os.path.join(dir, row + '.txt'), 'r')
    l=fp1.readlines()
    print(l,dir)
    l=l[0].split(",")
    l=[int(i) for i in l]
    for i in seats:
        if(l[i]==1):
            l[i]=0
        if(l[i]==2):
            l[i]=2
    li = [str(i) for i in l]
    temp = ",".join(li)
    fp = open(os.path.join(dir, row + '.txt'), 'w')
    fp.write(temp)




@api_view(["POST"])
def reserve(request,slug):
    seats=request.data.get("seats")
    for (k,v) in seats.items():
        doReservation(slug,k,v)


def getSeatsInfo(dir,filename):
    fp1 = open(os.path.join(dir, filename), 'r')
    l=fp1.readlines()
    l=l[0].split(",")
    l=[int(i) for i in l]
    res=[]
    for i in range(0,len(l)):
        if(l[i]==1 or l[i]==2):
            res.append(i)
    return res



@api_view(["GET"])
def unreservedSeats(request,slug):
    z="./"+slug
    filesList=os.listdir(z)
    result={}
    for i in filesList:
        result[i[:len(i)-4]]=getSeatsInfo(slug,i)
    return JsonResponse(result)

def isContinous(i,l,k):
    temp=l[i:i+k]
    for i in range(0,len(temp)):
        if(temp[i]==0 or temp[i]==3):
            return 0;
        elif((temp[i]==2 and (i>0 and i<=len(temp)-1))):
            return 0
    return 1

def getSeats(slug,noOfSeats,choice):
    fileName=choice[0]+".txt"
    choice=int(choice[1:])
    fp1 = open(os.path.join(slug, fileName), 'r')
    l=fp1.readlines()
    l=l[0]
    l=l.split(",")
    l=[int(i) for i in l]
    for i in range(abs(choice-noOfSeats+1),choice+1):
        if(isContinous(i,l,noOfSeats)):
            return i
    return -1




@api_view(["GET"])
def getChoiceBasedSeats(request,slug,noOfSeats,choice):
    t=getSeats(slug,noOfSeats,choice)
    li=list(range(t,t+noOfSeats))
    di={}
    di[choice[0]]=li
    return JsonResponse({"availableSeats":di})