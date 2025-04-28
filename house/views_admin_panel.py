import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods

from .forms import PropertyForm
from .models import PropertyType, DealType, Feature, PropertyImage, Property


def is_admin(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_admin, login_url='/admin-panel/login/')
def admin_dashboard(request):
    properties = Property.objects.all().select_related("property_type", "deal_type")
    property_types = PropertyType.objects.all()
    deal_types = DealType.objects.all()
    features = Feature.objects.all()

    return render(request, "admin_panel/dashboard.html", {
        "properties": properties,
        "property_types": property_types,
        "deal_types": deal_types,
        "features": features,
    })


def dashboard(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property = form.save()
            return redirect('custom_admin')  # оновлення списку
    else:
        form = PropertyForm()

    properties = Property.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/dashboard.html', {
        'form': form,
        'properties': properties
    })


def property_images_api(request, pk):
    images = PropertyImage.objects.filter(property_id=pk)
    data = [{"url": img.image.url, "is_main": img.is_main} for img in images]
    return JsonResponse(data, safe=False)


@require_POST
def delete_property(request, pk):
    property = get_object_or_404(Property, pk=pk)
    property.delete()
    return redirect('custom_admin')


@csrf_exempt
@require_http_methods(["PATCH"])
def patch_property(request, pk):
    try:
        prop = Property.objects.get(pk=pk)
        data = json.loads(request.body)

        if "title" in data:
            prop.title = data["title"]

        if "address" in data:
            prop.address = data["address"]

        if "rooms" in data and str(data["rooms"]).isdigit():
            prop.rooms = int(data["rooms"])

        if "deal_type" in data:
            try:
                deal_type_id = int(data["deal_type"]) if not isinstance(data["deal_type"], dict) else int(
                    data["deal_type"].get("id"))
                prop.deal_type = DealType.objects.get(pk=deal_type_id)
            except (ValueError, TypeError, DealType.DoesNotExist):
                return JsonResponse({"status": "error", "message": "DealType not found"}, status=400)

        if "property_type" in data:
            try:
                property_type_id = int(data["property_type"]) if not isinstance(data["property_type"], dict) else int(
                    data["property_type"].get("id"))
                prop.property_type = PropertyType.objects.get(pk=property_type_id)
            except (ValueError, TypeError, PropertyType.DoesNotExist):
                return JsonResponse({"status": "error", "message": "PropertyType not found"}, status=400)

        if "area" in data and data["area"] not in [None, ""]:
            try:
                prop.area = float(data["area"])
            except ValueError:
                pass  # можна залогувати

        if "price" in data and data["price"] not in [None, ""]:
            try:
                prop.price = float(data["price"])
            except ValueError:
                pass

        prop.save()

        # Optional: оновити головне фото
        if "main_photo_ids" in data:
            PropertyImage.objects.filter(property=prop).update(is_main=False)
            PropertyImage.objects.filter(id__in=data["main_photo_ids"]).update(is_main=True)

        return JsonResponse({"status": "ok"})

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('/admin-panel/dashboard/')
        else:
            error = "Невірне ім’я користувача або пароль"
    return render(request, 'admin_panel/login.html', {'error': error})
