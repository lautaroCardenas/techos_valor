from django.shortcuts import render

def not_found(request, exception=None):
    return render(request, 'not_found.html', status=404)