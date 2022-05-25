from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from control.models import Movies as m,Like,Dislike,Favorite
from django.views.decorators.csrf import csrf_exempt

def index(request):
    movies = m.objects.all()
    return render(request, 'index.html',{'movies':movies})
@csrf_exempt
def addto(request):
    if request.method == 'POST':
        type = request.POST['type']
        movie = request.POST['mid']
        print(type,movie)
        if type == 'like':
            obj = m.objects.get(id = movie)
            like = Like(name = obj.name,mid = obj.id)
            obj.like = True
            if obj.dislike:
                obj.dislike = False
                t = Dislike.objects.get(mid = obj.id)
                t.delete()
            obj.save()
            like.save()
        elif type == 'dislike':
            obj = m.objects.get(id = movie)
            dislike = Dislike(name = obj.name,mid = obj.id)
            obj.dislike = True
            if obj.like:
                obj.like = False
                t = Like.objects.get(mid = obj.id)
                t.delete()
            obj.save()
            dislike.save()
        elif type == 'watch':
            obj = m.objects.get(id = movie)
            fav = Favorite(name = obj.name,mid = obj.id)
            obj.watch = True
            obj.save()
            fav.save()
        elif type == 'dislike->like':
            obj = m.objects.get(id = movie)
            d_l = Dislike.objects.get(mid = obj.id)
            obj.like = True
            obj.dislike = False
            newobj = Like(name = obj.name, mid = obj.id)
            newobj.save()
            obj.save()
            d_l.delete()
        elif type == 'like->dislike':
            obj = m.objects.get(id = movie)
            d_l = Dislike.objects.get(mid = obj.id)
            obj.like = False
            obj.dislike = True
            newobj = Dislike(name = obj.name, mid = obj.id)
            newobj.save()
            obj.save()
            d_l.delete()
        elif type == 'watch->remove':
            obj = m.objects.get(id = movie)
            w_r = Favorite.objects.get(mid = obj.id)
            obj.watch = False
            obj.save()
            w_r.delete()
        return HttpResponse("done")
def like(request):
    objs = Like.objects.all()
    movies = []
    for i in objs:
        movies.append(m.objects.get(id = i.mid))
    return render(request, 'like.html',{'movies':movies})
def dislike(request):
    objs = Dislike.objects.all()
    movies = []
    for i in objs:
        movies.append(m.objects.get(id = i.mid))
    return render(request, 'dislike.html',{'movies':movies})
def watch(request):
    objs = Favorite.objects.all()
    movies = []
    for i in objs:
        movies.append(m.objects.get(id = i.mid))
    return render(request, 'watch.html',{'movies':movies})

def reset(request):
    favobj = Favorite.objects.all()
    likeobj = Like.objects.all()
    dislikeobj = Dislike.objects.all()
    mobj = m.objects.all()
    for movie in mobj:
        movie.like = False
        movie.dislike = False
        movie.watch = False
        movie.save()
    favobj.delete()
    likeobj.delete()
    dislikeobj.delete()
    return redirect('/')

def movie(request):
    if request.method == 'GET':
        id = request.GET['movie_id']
        movie_particularly = m.objects.get(id=id)
        return render(request, 'movie.html',{"obj":movie_particularly})
