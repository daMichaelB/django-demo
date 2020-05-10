from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from common.decorators import ajax_required
from images.forms import ImageCreateForm
from images.models import Image


@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # WE USE OUR OWN FUNCTION HERE, that downloads the actual image
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()

            messages.success(request, 'Image added successfully')

            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)
    return render(request, 'images/image/create.html', {'section': 'images', 'form': form})


@login_required
def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    print(request)
    return render(request, 'images/image/detail.html', {'section': 'images', 'image': image})


@ajax_required
@login_required
@require_POST  # only allow POST's for this view, returns 405 if Method != POST
def image_like(request):
    image_id = request.POST.get("id")
    action = request.POST.get("action")  # action should be a string of "like" or "unlike"
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                print("add users like")
                image.users_like.add(request.user)  # .add() working for many-to-many relationship
            else:
                image.users_like.remove(request.user)  # .remove() working for many-to-many relationship
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            print(str(e))
    # Finally, you use the JsonResponse class provided by Django, which returns an HTTP response with an
    # application/json content type, converting the given object into a JSON output.
    return JsonResponse({'status': 'error'})


@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')

    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an int deliver the first page
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # If the request is AJAX and the page is out of range return an empty page
            # this is to stop pagination on client side
            return HttpResponse('')
        # If page is out of range deliver last page of results
        images = paginator.page(paginator.num_pages)

    if request.is_ajax():
        # this template only contains the new images
        return render(request, 'images/image/list_ajax.html', {'section': 'images', 'images': images})

    # this is the big template deriving from base.html
    return render(request, 'images/image/list.html', {'section': 'images', 'images': images})
