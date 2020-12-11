from django.shortcuts import render, get_object_or_404, redirect
from .models import News
from main.models import Main
from subcat.models import SubCat
from django.core.files.storage import FileSystemStorage
import datetime
from cat.models import Cat
from trending.models import Trending

# Create your views here.

def news_detail(request,word):

    site = Main.objects.get(pk=1)
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    news = News.objects.all().order_by('-pk')
    lastnews = News.objects.all().order_by('-pk')[:3]
    popnews = News.objects.all().order_by('-show')
    popnews2 = News.objects.all().order_by('-show')[:3]
    trending = Trending.objects.all()

    shownews = News.objects.filter(name=word)

    tagnames = News.objects.get(name=word).tag
    tag = tagnames.split(',')
    try: 
        mynews = News.objects.get(name=word)
        mynews.show = mynews.show + 1
        mynews.save()
    except:
        print('view counter bug')

    return render(request, 'front/news_detail.html', {'site' : site, 'shownews' : shownews, 'cat':cat, 'subcat':subcat, 'news' : news, 'lastnews' : lastnews, 'popnews' : popnews, 'popnews2' : popnews2, 'tag' : tag, 'trending':trending})


def news_list(request):
    
    #login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #login check end
    
    news = News.objects.all()
    return render(request, 'back/news_list.html',{'news':news})

def news_add(request):

    #login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #login check end

    cat = SubCat.objects.all()

    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day

    if len(str(day)) == 1:
        day = "0" + str(day)
    if len(str(month)) == 1:
        month = "0" + str(month)

    today = str(year) + "/" + str(month) + "/" + str(day)

    current_time = str(now.hour) + ":" + str(now.minute)

    if request.method == 'POST':
        newstitle = request.POST.get('newstitle')
        newstxtshort = request.POST.get('newstxtshort')
        newstxt = request.POST.get('newstxt')
        newscatid = request.POST.get('newscat')
        newscat = SubCat.objects.get(pk=newscatid)
        newstag = request.POST.get('tag')

        if newstitle == "" or newscat == "" or newstxtshort == "" or newstxt == "":
            error = "All Fields are required"
            return render(request, 'back/error.html',{'error':error})

        try:

            newsfile = request.FILES['newsimg']
            fs = FileSystemStorage()
            filename = fs.save(newsfile.name, newsfile)
            url = fs.url(filename)

            if str(newsfile.content_type).startswith('image'):

                if newsfile.size < 5000000:
                    
                    newsname = SubCat.objects.get(pk=newscatid).name
                    ocatid = SubCat.objects.get(pk=newscatid).catid

                    b = News(name=newstitle, short_txt=newstxtshort, body_txt=newstxt, date=today, time=current_time, picname=filename, picurl=url, writer="-", catname=newscat, catid=newscatid, show=0, ocatid=ocatid, tag=tag)
                    b.save()

                    count = len(News.objects.filter(ocatid=ocatid))

                    b = Cat.objects.get(pk=ocatid)
                    b.count = count
                    b.save()

                    return redirect('news_list')
                
                else:

                    fs = FileSystemStorage()
                    fs.delete(filename)

                    error = "Your File Is Bigger Then 5 MB"
                    return render(request, 'back/error.html',{'error':error})

            else:

                fs = FileSystemStorage()
                fs.delete(filename)

                error = "Your File Not Supported"
                return render(request, 'back/error.html',{'error':error})    

        except:

            error = "please select image for news."
            return render(request, 'back/error.html',{'error':error})

    return render(request, 'back/news_add.html',{'cat':cat})

def news_delete(request,pk):

    #login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #login check end

    try:
        news = News.objects.get(pk=pk) 
        # to delete files
        fs = FileSystemStorage()
        fs.delete(news.picname)

        ocatid = News.objects.get(pk=pk).ocatid

        news.delete()
    
        count = len(News.objects.filter(ocatid=ocatid))

        m = Cat.objects.get(pk=ocatid)
        m.count = count
        m.save()



    except:
        error = "Something Wrong."
        return render(request, 'back/error.html',{'error':error})


    return redirect('news_list')


def news_edit(request,pk):

    #login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #login check end

    if len(News.objects.filter(pk=pk)) == 0:
        error = "News Not Found"
        return render(request, 'back/error.html',{'error':error})



    cat = SubCat.objects.all()

    if request.method == 'POST':
        newstitle = request.POST.get('newstitle')
        newstxtshort = request.POST.get('newstxtshort')
        newstxt = request.POST.get('newstxt')
        newscatid = request.POST.get('newscat')
        newstag = request.POST.get('tag')
        newscat = SubCat.objects.get(pk=newscatid)

        if newstitle == "" or newscat == "" or newstxtshort == "" or newstxt == "":
            error = "All Fields are required"
            return render(request, 'back/error.html',{'error':error})

        try:

            newsfile = request.FILES['newsimg']
            fs = FileSystemStorage()
            filename = fs.save(newsfile.name, newsfile)
            url = fs.url(filename)

            if str(newsfile.content_type).startswith('image'):

                if newsfile.size < 5000000:
                    
                    newscat = SubCat.objects.get(pk=newscatid).name
                    
                    b = News.objects.get(pk=pk)
                    
                    fss = FileSystemStorage()
                    fss.delete(b.picname)
                    
                    b.name = newstitle
                    b.short_txt = newstxtshort
                    b.body_txt = newstxt
                    b.filename = filename
                    b.picurl = url
                    b.writer = '-'
                    b.tag = newstag
                    b.catname = newscat 
                    b.catid = newscatid
                    b.save()
                    return redirect('news_list')
                
                else:

                    fs = FileSystemStorage()
                    fs.delete(filename)

                    error = "Your File Is Bigger Then 5 MB"
                    return render(request, 'back/error.html',{'error':error})

            else:

                fs = FileSystemStorage()
                fs.delete(filename)

                error = "Your File Not Supported"
                return render(request, 'back/error.html',{'error':error})    

        except:
            newscat = SubCat.objects.get(pk=newscatid).name

            b = News.objects.get(pk=pk)
            b.name = newstitle
            b.short_txt = newstxtshort
            b.body_txt = newstxt
            b.tag = newstag
            b.catname = newscat 
            b.catid = newscatid
            b.save()
            return redirect('news_list')


    news = News.objects.get(pk=pk)
    return render(request, 'back/news_edit.html',{'pk':pk, 'news':news, 'cat':cat})
