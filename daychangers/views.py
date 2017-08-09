from django.shortcuts import render
from .nse import Nse
from urllib.request import build_opener, HTTPCookieProcessor, Request
from django.http import HttpResponse
from django.shortcuts import get_object_or_404,redirect
from django.http import Http404
from django.contrib.auth import authenticate, login,logout
from django.views import generic 
from django.views.generic import View
from django.contrib.sessions.backends.db import SessionStore
from .forms import UserForm
from .models import Orderbook
from .models import Ordernumber
from .models import Stockspecific
from .models import Margin
from .models import Stocksearch
from .models import Addedscript
from .models import Pendingorder
from urllib.parse import urlencode
import requests
import json
import pytz
import collections
import datetime
import decimal
import csv
import datetime

def index(request):
    """
        return: send the user to the login page after login
    """
    nse = Nse()
    gainer=nse.get_top_gainers()
    loser=nse.get_top_losers()
    username = request.user
    mar=Margin.objects.filter(user=username)
    script=Addedscript.objects.filter(user=username)
    return render(request, 'daychangers/dashboard.html',{'gainer':gainer, 'loser':loser,'margin':mar,'user':username,'script':script} )    

def register(request):
    """
        Register the client and allot margin of 1 lakh initially
        Saving one script initially on all client register, so exception is not raised 
    """
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        nse = Nse()
        user.save()
        fund_available=Margin(funds=100000,user=username,holdings=0)
        fund_available.save()
        detail=nse.get_quote("SBIN")
        add=Addedscript(name="SBIN",user=username,ltp=detail['lastPrice'])
        add.save()
        return render(request, 'daychangers/redlogin.html')
    context = {
            "form": form,
        }
    return render(request, 'daychangers/registration_form.html',{'form': form,} )    

def login_user(request):
    """
       Authenticating the user login using django authenticate 
    """
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)  
            request.session['user_name']=username
            mar=Margin.objects.filter(user=username)
            nse=Nse()
            gainer=nse.get_top_gainers()
            loser=nse.get_top_losers()
            return redirect('http://gainerandloser.herokuapp.com/index/')

        else:    
            return render(request, 'daychangers/login.html',{'error_message': 'Go and Create new account'})   

    else:   
        return render(request, 'daychangers/login.html')  

def logout_user(request):
    """
       Deleting the session login  
    """
    logout(request) 
    return render(request, 'daychangers/login.html')
            
def checkorder(request):
    """
       Order placement module, storing the detail in orderbook models  
    """
            if request.method == "POST":        
                stock_name= request.POST['place']

            if request.method=="POST":
                qua=request.POST['quantity']

            if request.method=="POST":
                ortype=request.POST['order']       

            nse=Nse()
            getquote=nse.get_quote(stock_name)
            order_number=Ordernumber.objects.all()
            for ord in order_number:
                ordr=ord
                order_no=ord.number+1
            user = request.user
            if ortype == "market":
                order= Orderbook(client_id=user,symbol=stock_name,price=getquote['lastPrice'],quantity=1,date=datetime.datetime.now(tz=pytz.timezone('Asia/Calcutta')),trade_type='BUY',orderno=order_no,ordertype=ortype, status="success")
                order.save()

            else:    
                if float(qua) >= getquote['lastPrice']:
                    order= Orderbook(client_id=user,symbol=stock_name,price=qua,quantity=1,date=datetime.datetime.now(tz=pytz.timezone('Asia/Calcutta')),trade_type='BUY',orderno=order_no,ordertype=ortype, status="success")
                    order.save()
                else:
                    order= Pendingorder(client_id=user,symbol=stock_name,price=qua,quantity=1,date=datetime.datetime.now(tz=pytz.timezone('Asia/Calcutta')),trade_type='BUY',orderno=order_no,ordertype=ortype,status="pending")
                    order.save()

            number=Ordernumber(number=order_no)
            number.save()
            holding_value = getquote['lastPrice']*1
            detail=Margin.objects.filter(user=user)
            q=Orderbook.objects.filter(client_id=user)
            q1=Pendingorder.objects.filter(client_id=user)
            for checks in q1:
                if checks.status == "pending":
                    sym=nse.get_quote(checks.symbol)
                    if checks.price >= decimal.Decimal(sym['lastPrice']):
                        order= Orderbook(client_id=user,symbol=checks.symbol,price=sym['lastPrice'],quantity=1,date=datetime.datetime.now(tz=pytz.timezone('Asia/Calcutta')),trade_type='BUY',orderno=order_no,ordertype=ortype, status="success")
                        order.save()
                        move=Pendingorder.objects.filter(client_id=user,symbol=checks.symbol)
                        move.delete()


            for inspect in detail:
                fund_update=decimal.Decimal(inspect.funds) - decimal.Decimal(holding_value)
                holdingval=decimal.Decimal(100000) - decimal.Decimal(fund_update)
                Margin.objects.filter(user=user).update(holdings=holdingval,funds=fund_update)
            return redirect('https://gainerandloser.herokuapp.com/orders') 
def orders(request):
    """
       This page keep on refreshing as per ajax request, and convert the pending order to completed
       order, as per order type 
    """
        user = request.user
        nse=Nse()
        q=Orderbook.objects.filter(client_id=user)
        q1=Pendingorder.objects.filter(client_id=user)
        order_number=Ordernumber.objects.all()
        for ord in order_number:
                ordr=ord.number

        for checks in q1:
            if checks.status == "pending":
                sym=nse.get_quote(checks.symbol)
                if checks.price >= decimal.Decimal(sym['lastPrice']):
                    order= Orderbook(client_id=user,symbol=checks.symbol,price=sym['lastPrice'],quantity=1,date=datetime.datetime.now(tz=pytz.timezone('Asia/Calcutta')),trade_type='BUY',orderno= ordr,ordertype="limit", status="success")
                    order.save()
                    move=Pendingorder.objects.filter(client_id=user,symbol=checks.symbol)
                    move.delete()
                  
        return render(request, 'daychangers/logtest.html',{'i_d':q,'q1':q1,})




def addsymbol(request): 
    """
       Add the script in real time to marketwatch 
    """
    stock=request.GET['stock']
    nse=Nse()
    user = request.user
    detail=nse.get_quote(stock)
    add=Addedscript(name=stock,user=user,ltp=detail['lastPrice'])
    add.save() 
    return HttpResponse(detail['lastPrice'])

def holding(request):  
    """
       retrives the holding from orderbook 
    """
    nse=Nse()   
    user = request.user
    hold=Orderbook.objects.filter(client_id=user) 
    if hold:
        for detail in hold: 
            detail=nse.get_quote(detail.symbol)
            return render(request, 'daychangers/holding.html',{'i_d':hold,'detail':detail})  
    else:
        return render(request, 'daychangers/holding.html',{'msg':'no holdings'},)                                   