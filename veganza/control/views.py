from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
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
        obj = m.objects.get(id = movie)
        if type == 'like':
            like = Like(name = obj.name,mid = obj.id)
            obj.like = True
            obj.save()
            like.save()
        elif type == 'dislike':
            dislike = Dislike(name = obj.name,mid = obj.id)
            obj.dislike = True
            obj.save()
            dislike.save()
        elif type == 'watch':
            fav = Favorite(name = obj.name,mid = obj.id)
            obj.watch = True
            obj.save()
            fav.save()
        return HttpResponse("done")
