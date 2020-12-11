from django.shortcuts import render, get_object_or_404, redirect
from .models import Main
from news.models import News
from cat.models import Cat
from subcat.models import SubCat
from manager.models import Manager
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from trending.models import Trending
import random
from random import randint
from django.contrib.auth.models import User, Group, Permission

# Create your views here.

def home(request):
    site = Main.objects.get(pk=1)
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    news = News.objects.filter(act=1).order_by('-pk')
    lastnews = News.objects.filter(act=1).order_by('-pk')[:3]
    popnews = News.objects.filter(act=1).order_by('-show')
    popnews2 = News.objects.filter(act=1).order_by('-show')[:3]
    trending = Trending.objects.all()[:5]

    random_object = Trending.objects.all()[randint(0, len(trending) - 1)]
    print(random_object)

    return render(request, 'front/home.html', {'site' : site, 'cat':cat, 'subcat':subcat, 'news' : news, 'lastnews' : lastnews,  'popnews' : popnews, 'popnews2' : popnews2, 'trending':trending})

def about(request):

    site = Main.objects.get(pk=1)
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    news = News.objects.all().order_by('-pk')
    lastnews = News.objects.all().order_by('-pk')[:3]
    popnews2 = News.objects.all().order_by('-show')[:3]
    trending = Trending.objects.all()
    
    return render(request, 'front/about.html', {'site' : site, 'cat':cat, 'subcat':subcat, 'news' : news, 'lastnews' : lastnews, 'popnews2' : popnews2, 'trending':trending})

def panel(request):

    #login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #login check end

    perm = 0 
    perms = Permission.objects.filter(user=request.user)
    for i in perms:
        if i.codename == "master_user" : perm = 1
    if perm == 0:
        error = "Access Denied"
        return render(request, 'back/error.html',{'error':error})        

    site = Main.objects.get(pk=1)
    
    return render(request, 'back/home.html', {'site' : site})

def mylogin(request):

    if request.method == 'POST':
        utxt = request.POST.get('username')
        ptxt = request.POST.get('password')

        if utxt != "" and ptxt != "":

            user = authenticate(username=utxt,password=ptxt)

            if user != None:

                login(request,user)
                return redirect('panel')

    return render(request, 'front/login.html')

def mylogout(request):

    logout(request)

    return redirect('mylogin')

def site_setting(request):

    #login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #login check end

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0:
        error = "Access Denied"
        return render(request, 'back/error.html',{'error':error})

    if request.method == 'POST':
        name = request.POST.get('name')
        tell = request.POST.get('tell')
        fb = request.POST.get('fb')
        tw = request.POST.get('tw')
        yt = request.POST.get('yt')
        link = request.POST.get('link')
        txt = request.POST.get('about')

        if fb == "" : fb = '#'
        if tw == "" : tw = '#'
        if yt == "" : yt = '#'
        if link == "" : link = '#'

        if name == "" or tell == "" or txt == "":
            error = "All Fields Required"
            return render(request, 'back/error.html',{'error':error})

        try:

            myfile = request.FILES['logo_header']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)

            picurl = url
            picname = filename

        except:

            picurl = '#'
            picname = '-'

        try:

            myfile2 = request.FILES['logo_footer']
            fs2 = FileSystemStorage()
            filename2 = fs2.save(myfile2.name, myfile2)
            url2 = fs2.url(filename2)

            picurl2 = url2
            picname2 = filename2

        except:

            picurl2 = '#'
            picname2 = '-'

        b = Main.objects.get(pk=1)
        b.name = name
        b.tell = tell
        b.fb = fb
        b.tw = tw
        b.yt = yt
        b.link = link
        b.about = txt
        if picurl != "#" : b.picurl = picurl  
        if picname != "-" : b.picname = picname 
        if picurl2 != "#" : b.picurl2 = picurl2  
        if picname2 != "-" : b.picname2 = picname2 
        
        b.save()

    site = Main.objects.get(pk=1)

    return render(request, 'back/setting.html',{'site':site})


def about_setting(request):

    #login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #login check end

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0:
        error = "Access Denied"
        return render(request, 'back/error.html',{'error':error})



    if request.method == "POST":
        txt = request.POST.get('txt')

        if txt == "":
            error = "All fields are required"
            return render(request, 'back/error.html',{'error':error})
            
        b = Main.objects.get(pk=1)
        b.abouttxt = txt
        b.save()

    about = Main.objects.get(pk=1).abouttxt

    return render(request, 'back/about_setting.html',{'about':about})

def contact(request):
    site = Main.objects.get(pk=1)
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    news = News.objects.all().order_by('-pk')
    lastnews = News.objects.all().order_by('-pk')[:3]
    popnews2 = News.objects.all().order_by('-show')[:3]
    trending = Trending.objects.all()


    return render(request, 'front/contact.html', {'site' : site, 'cat':cat, 'subcat':subcat, 'news' : news, 'lastnews' : lastnews, 'popnews2' : popnews2, 'trending':trending})


def change_pass(request):

    #login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #login check end

    if request.method == "POST":
        oldpass = request.POST.get('oldpass')
        newpass = request.POST.get('newpass')

        if oldpass == "" or newpass == "":
            error = "All Fields Required"
            return render(request, 'back/error.html',{'error':error})

        user = authenticate(username=request.user, password=oldpass)            

        if user != None:
            if len(newpass) < 8:
                error = "Your Password must be more then 8 Char"
                return render(request, 'back/error.html',{'error':error})    
            
            count1 = 0
            count2 = 0
            count3 = 0
            count4 = 0
            
            for i in newpass:
                
                if i >= "0" and i <= "9":
                    count1 = 1
                if i >= "A" and i <= "Z":
                    count2 = 1
                if i >= "a" and i <= "z":
                    count3 = 1
                if i >= "!" and i <= "(":
                    count4 = 1

            print(count1,count2,count3,count4)
            if count1 == 1 and count2 == 1 and count3 == 1 and count4 == 1 :
                user = User.objects.get(username = request.user)
                user.set_password(newpass)
                user.save()
                return redirect('mylogout')
            else:
                error = "Your Password must be Strong"
                return render(request, 'back/error.html',{'error':error})    
               


        else:
            error = "Your password is incorrect"
            return render(request, 'back/error.html',{'error':error})

    return render(request, 'back/changepass.html')

def myregister(request):

    if request.method == "POST":
        name = request.POST.get('name')
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            msg = "Your password did not match"
            return render(request,'front/msgbox.html',{'msg':msg})

            
        count1 = 0
        count2 = 0
        count3 = 0
        count4 = 0
        
        for i in password1:
            
            if i >= "0" and i <= "9":
                count1 = 1
            if i >= "A" and i <= "Z":
                count2 = 1
            if i >= "a" and i <= "z":
                count3 = 1
            if i >= "!" and i <= "(":
                count4 = 1

        print(count1,count2,count3,count4)
        if count1 == 0 and count2 == 0 and count3 == 0 and count4 == 0 :
            msg = "Your password is not strong"
            return render(request,'front/msgbox.html',{'msg':msg})
            
        if len(password1) < 8:
            msg = "Your password must be 8 Char"
            return render(request,'front/msgbox.html',{'msg':msg})

        if len(User.objects.filter(username=uname)) == 0 and len(User.objects.filter(email=email)) == 0:

            user = User.objects.create_user(username=uname,email=email,password=password1)
            b = Manager(name=name, utxt=uname, email=email)
            b.save()
            
    return render(request, 'front/login.html')
