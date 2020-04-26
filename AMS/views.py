from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import LoginForm
from admin_panel.models import Login

def logout(request):
    request.session['user_id'] = None
    return redirect('/')
    
def login(request):

    if request.method=='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['name']
            password = form.cleaned_data['pwd']
            users = Login.objects.filter(username=username,password=password)
            if users is not None and len(users)>0:
                
                request.session['user_id'] = users[0].id
                request.session['type'] = users[0].usertype
                if users[0].usertype=='teacher':
                    return redirect('teacher_panel/',{'user':users[0]})
                return redirect('admin_panel/',{'user':users[0]})
            else:
                context = {'error_message': 'Username or password is not correct.','form':form}
                return render(request,'login.html',context)
    else:
        form = LoginForm()
        return render(request,'login.html',{'form':form})

