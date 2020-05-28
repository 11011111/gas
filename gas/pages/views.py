from django.shortcuts import render, redirect

# Create your views here.
def main_page(request):

    return render(request, 'pages/main.html', locals())
    # return redirect('/auth/login/')
