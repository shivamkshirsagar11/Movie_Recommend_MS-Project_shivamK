from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from control.models import Movies as m,Like,Dislike,Favorite,Recommend
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

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
    recommendobj = Recommend.objects.all()
    mobj = m.objects.all()
    for movie in mobj:
        movie.like = False
        movie.dislike = False
        movie.watch = False
        movie.save()
    favobj.delete()
    likeobj.delete()
    dislikeobj.delete()
    recommendobj.delete()
    return redirect('/')

def movie(request):
    if request.method == 'GET':
        id = request.GET['movie_id']
        movie_particularly = m.objects.get(id=id)
        return render(request, 'movie.html',{"obj":movie_particularly})

def recommend(request):
    objs = Recommend.objects.all()
    movies = []
    for i in objs:
        movies.append(m.objects.get(id = i.mid))
    return render(request, 'recommend.html',{'movies':movies})
@csrf_exempt
def process(request):
    if request.method == 'POST':
        movie_id = request.POST['mid']
        mobj = m.objects.get(id=movie_id)
        process_movie_recommendations(mobj.category,mobj.actors)
        return HttpResponse('okay')

def common(list1,list2):
    temp = []
    for i in list2:
        if i in list1:
            temp.append(i)
    return temp
def not_common(list1,list2):
    temp = []
    for i in list2:
        if i not in list1:
            temp.append(i)
    for i in list1:
        if i not in list2:
            temp.append(i)
    return temp

def add_to_database_recommend(recommend_movie_ids):
    for i in recommend_movie_ids:
        temp = Recommend(mid = i)
        temp.save()

def process_movie_recommendations(categories,actors):
    categories = categories.split(', ')
    actors = actors.split(', \r\n')
    # print (categories, actors)
    movie_rec_list_1 = []
    movie_rec_list_1_1 = []
    movie_rec_list_1_2 = []
    movie_rec_list_1_3 = []
    movie_rec_list_2 = []
    #------------------------------------------------------------------------------------------
    for i in categories:
        temp = m.objects.filter(category__icontains = i)
        for temp2 in temp:
            if temp2.id not in movie_rec_list_1: movie_rec_list_1.append(temp2.id)
    #------------------------------------------------------------------------------------------
    temp_1 = m.objects.filter(Q(category__icontains =categories[0]) & Q(category__icontains = categories[1]))
    temp_2 = m.objects.filter(Q(category__icontains =categories[1]) & Q(category__icontains = categories[2]))
    temp_3 = m.objects.filter(Q(category__icontains =categories[2]) & Q(category__icontains = categories[0]))
    print(temp_1,temp_2,temp_3)
    for i in temp_1:
        movie_rec_list_1_1.append(i.id)
    for i in temp_2:
        movie_rec_list_1_2.append(i.id)
    for i in temp_3:
        movie_rec_list_1_3.append(i.id)
    #------------------------------------------------------------------------------------------
    for index,actor in enumerate(actors):
        temp = m.objects.filter(actors__icontains = actor)
        for temp2 in temp:
            if temp2.id not in movie_rec_list_2: movie_rec_list_2.append(temp2.id)
    #------------------------------------------------------------------------------------------

    movie_recommend_final_common = common(movie_rec_list_2,movie_rec_list_1)
    add_to_database_recommend(movie_recommend_final_common)
    temp_4 = []
    for i in movie_rec_list_1_1:
        if (i not in movie_recommend_final_common):
            temp_4.append(i)
    for i in movie_rec_list_1_2:
        if (i not in temp_4) and (i not in movie_recommend_final_common):
            temp_4.append(i)
    for i in movie_rec_list_1_3:
        if (i not in temp_4) and (i not in movie_recommend_final_common):
            temp_4.append(i)
    print(temp_4)
    add_to_database_recommend(temp_4)
            
    movie_rec_list_1.clear()
    movie_rec_list_1_1.clear()
    movie_rec_list_1_2.clear()
    movie_rec_list_1_3.clear()
    movie_rec_list_2.clear()
    movie_recommend_final_common.clear()