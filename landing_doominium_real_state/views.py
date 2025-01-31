from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


# def action_for_owners(request):
#     return render(request, 'action_for_owners.html')
