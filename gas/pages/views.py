from django.shortcuts import render, redirect

# Create your views here.
def main_page(request):

    return render(request, 'pages/main.html', locals())
    # return redirect('/auth/login/')

def form_page(request):
    a = 100
    return render(request, 'pages/form.html', locals())