from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from control.models import Movies as m,Like,Dislike,Favorite,Recommend,info
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
        # print(type,movie)
        if type == 'like':
            obj = m.objects.get(id = movie)
            process_movie_recommendations(obj.category,obj.actors,obj.director,obj.studio)
            old_obj_removing = info.objects.all()
            old_obj_removing.delete()
            new_obj_add = info(what_action_performed = "Because You Liked "+obj.name+" !")
            new_obj_add.save()
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
            rec = Recommend.objects.filter(mid = obj.id)
            rec = rec.first()
            if rec != None :rec.delete()
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
            process_movie_recommendations(obj.category,obj.actors,obj.director,obj.studio)
            old_obj_removing = info.objects.all()
            old_obj_removing.delete()
            new_obj_add = info(what_action_performed = "Because You Added "+obj.name+" To your Watch-List !")
            new_obj_add.save()
            fav = Favorite(name = obj.name,mid = obj.id)
            obj.watch = True
            obj.save()
            fav.save()
        elif type == 'dislike->like':
            obj = m.objects.get(id = movie)
            process_movie_recommendations(obj.category,obj.actors,obj.director,obj.studio)
            old_obj_removing = info.objects.all()
            old_obj_removing.delete()
            new_obj_add = info(what_action_performed = "Because You Liked "+obj.name+" !")
            new_obj_add.save()
            d_l = Dislike.objects.get(mid = obj.id)
            obj.like = True
            obj.dislike = False
            newobj = Like(name = obj.name, mid = obj.id)
            newobj.save()
            obj.save()
            d_l.delete()
        elif type == 'like->dislike':
            obj = m.objects.get(id = movie)
            rec = Recommend.objects.get(mid = obj.id)
            rec.delete()
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
        elif type == 'recommend->remove':
            OBJ = Recommend.objects.get(mid = movie)
            OBJ.delete()
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
    infos = info.objects.all()
    for movie in mobj:
        movie.like = False
        movie.dislike = False
        movie.watch = False
        movie.save()
    favobj.delete()
    likeobj.delete()
    dislikeobj.delete()
    recommendobj.delete()
    infos.delete()
    return redirect('/')

def movie(request):
    if request.method == 'GET':
        id = request.GET['movie_id']
        movie_particularly = m.objects.get(id=id)
        return render(request, 'movie.html',{"obj":movie_particularly})

def recommend(request):
    objs = Recommend.objects.all()
    infoObj = info.objects.all()
    second = ""
    for i in infoObj:second = i.what_action_performed
    movies = []
    for i in objs:
        movies.append(m.objects.get(id = i.mid))
    reverse_movie = []
    for i in range(len(movies)):
        reverse_movie.append(movies[(len(movies)-1)-i])
    return render(request, 'recommend.html',{'movies':reverse_movie,"info":second})
@csrf_exempt
def process(request):
    if request.method == 'POST':
        movie_id = request.POST['mid']
        mobj = m.objects.get(id=movie_id)
        old_obj_removing = info.objects.all()
        old_obj_removing.delete()
        new_obj_add = info(what_action_performed = "Because You Watched "+mobj.name+" !")
        new_obj_add.save()
        process_movie_recommendations(mobj.category,mobj.actors,mobj.director,mobj.studio)
        return HttpResponse('okay')

def clean_up():
    objs = Recommend.objects.all()
    if len(objs) >= 15:objs.delete()

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
    try:
        all_recommendations = []
        objs = Recommend.objects.all()
        objs_alpha = []
        for i in objs:objs_alpha.append(i.mid)
        for i in recommend_movie_ids:
            # print(i.id)
            if i not in objs_alpha: 
                all_recommendations.append(i)
        # print("at last sorted: ",all_recommendations)
        # print("passed objects parameter: ",recommend_movie_ids)
        # print("all recommend objects: ",objs_alpha)
        for i in all_recommendations:
            temp = Recommend(mid = i)
            temp.save()
    except:
        print("Something went wrong! please reset from browser and try again :-(")

def process_movie_recommendations(categories,actors,director,studio):
    clean_up()
    categories = categories.split(', ')
    actors = actors.split(', \r\n')
    studio = studio.split(', ')
    # print (categories, actors)
    movie_rec_list_1 = []
    movie_rec_list_1_1 = []
    movie_rec_list_1_2 = []
    movie_rec_list_1_3 = []
    movie_rec_list_1_4 = []
    movie_rec_list_1_5 = []
    movie_rec_list_1_6 = []
    movie_rec_list_2 = []
    movie_rec_list_3 = []
    movie_rec_list_4 = []
    #------------------------------------------------------------------------------------------
    d_ir = m.objects.filter(director__icontains=director)
    for i in d_ir:
        movie_rec_list_3.append(i.id)
    add_to_database_recommend(movie_rec_list_3)
    #------------------------------------------------------------------------------------------
    for i in studio:
        stu = m.objects.filter(studio__icontains=i)
        switch = 0
        # print(stu,i)
        for j in stu:
            j_act = j.actors
            j_act = j_act.split(', \r\n')
            j_cate = j.category
            j_cate  = j_cate.split(", ")
            # print(j_act)
            for k in j_act:
                # print(k)
                if k in actors:
                    # print(k)
                    switch = switch + 1
            if switch >= 1 and j.id not in movie_rec_list_4:
                if (j_cate[0] in categories) or (j_cate[1] in categories) or (j_cate[2] in categories):
                    movie_rec_list_4.append(j.id)
            # print(switch,movie_rec_list_4)
    #------------------------------------------------------------------------------------------
    for i in categories:
        temp = m.objects.filter(category__icontains = i)
        for temp2 in temp:
            if temp2.id not in movie_rec_list_1: movie_rec_list_1.append(temp2.id)
    #------------------------------------------------------------------------------------------
    #combination of 2-2 categories
    temp_1 = m.objects.filter(Q(category__icontains =categories[0]) & Q(category__icontains = categories[1])) 
    temp_2 = m.objects.filter(Q(category__icontains =categories[1]) & Q(category__icontains = categories[2]))
    temp_3 = m.objects.filter(Q(category__icontains =categories[2]) & Q(category__icontains = categories[0]))
    #combination of 1-1 category
    temp_1_beta = m.objects.filter(Q(category__icontains =categories[0]))
    temp_2_beta = m.objects.filter(Q(category__icontains =categories[1]))
    temp_3_beta = m.objects.filter(Q(category__icontains =categories[2]))

    # print(temp_1,temp_2,temp_3)
    # print(temp_1_beta,temp_2_beta,temp_3_beta)
    for i in temp_1:
        movie_rec_list_1_1.append(i.id)
    for i in temp_2:
        movie_rec_list_1_2.append(i.id)
    for i in temp_3:
        movie_rec_list_1_3.append(i.id)

    for i in temp_1_beta:
        check = i.category.split(', ')
        count = 0
        if (check[0] in categories and check[1] in categories) or (check[0] in categories and check[2] in categories) or (check[1] in categories and check[2] in categories): count = count + 1
        if count > 0:
            movie_rec_list_1_4.append(i.id)
    for i in temp_2_beta:
        check = i.category.split(', ')
        count = 0
        if (check[0] in categories and check[1] in categories) or (check[0] in categories and check[2] in categories) or (check[1] in categories and check[2] in categories): count = count + 1
        if count > 0:
            movie_rec_list_1_5.append(i.id)
    for i in temp_3_beta:
        check = i.category.split(', ')
        count = 0
        if (check[0] in categories and check[1] in categories) or (check[0] in categories and check[2] in categories) or (check[1] in categories and check[2] in categories): count = count + 1
        if count > 0:
            movie_rec_list_1_6.append(i.id)
    #------------------------------------------------------------------------------------------
    for index,actor in enumerate(actors):
        temp = m.objects.filter(actors__icontains = actor)
        for temp2 in temp:
            if temp2.id not in movie_rec_list_2: movie_rec_list_2.append(temp2.id)
    #------------------------------------------------------------------------------------------

    movie_recommend_final_common = common(movie_rec_list_2,movie_rec_list_1)
    # print(movie_rec_list_1)
    # print(movie_rec_list_2)
    # print(movie_rec_list_1_1)
    # print(movie_rec_list_1_2)
    # print(movie_rec_list_1_3)
    # print(movie_recommend_final_common)
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
    # print(temp_4)
    add_to_database_recommend(temp_4)

    one_to_one = []
    for i in movie_rec_list_1_4:
        if ((i not in movie_rec_list_1_5) or (i not in movie_rec_list_1_6)) and (i not in movie_recommend_final_common) and (i not in temp_4): one_to_one.append(i)
    for i in movie_rec_list_1_5:
        if ((i not in movie_rec_list_1_4) or (i not in movie_rec_list_1_6)) and (i not in movie_recommend_final_common) and (i not in one_to_one) and (i not in temp_4): one_to_one.append(i)
    for i in movie_rec_list_1_6:
        if ((i not in movie_rec_list_1_5) or (i not in movie_rec_list_1_4)) and (i not in movie_recommend_final_common) and (i not in one_to_one) and (i not in temp_4): one_to_one.append(i)
    add_to_database_recommend(one_to_one)
    add_to_database_recommend(movie_rec_list_4)
    # print(movie_rec_list_1_4)
    # print(movie_rec_list_1_5)
    # print(movie_rec_list_1_6)
    # print(one_to_one)

    movie_rec_list_1.clear()
    movie_rec_list_1_1.clear()
    movie_rec_list_1_2.clear()
    movie_rec_list_1_3.clear()
    movie_rec_list_1_4.clear()
    movie_rec_list_1_5.clear()
    movie_rec_list_1_6.clear()
    movie_rec_list_2.clear()
    movie_rec_list_3.clear()
    movie_rec_list_4.clear()
    movie_recommend_final_common.clear()
    print("Movies Processed and added to recommendations")