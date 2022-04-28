from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login,logout
from .models import *

def index(request):
    return render(request,'index.html')

def login(request):
    error=""
    if request.method=="POST":
        ur=request.POST['uname']
        pd=request.POST['pswd']
        user=auth.authenticate(username=ur,password=pd)
        try:
            if user.is_staff:
                auth.login(request,user)
                error="no"
            elif user is not None:
                auth.login(request,user)
                error="not"
            else:
                error="yes"
        except:
            error="yes"

    d={'error':error}
    return render(request,'login.html',d)

def signup(request):
    error=""
    if request.method=='POST':
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        c = request.POST['contact']
        dob = request.POST['dob']
        pd = request.POST['pwd']
        g = request.POST['gender']
        img = request.FILES['image']
        a = request.POST['add']
        try:
            user=User.objects.create_user(first_name=f,last_name=l,username=e,password=pd)
            Signup.objects.create(user=user,mobile=c,image=img,gender=g,dob=dob,address=a)
            error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request,'signup.html',d)

def admin_home(request):
    if not request.user.is_staff:
        return redirect('login')
    return render(request,'admin_home.html')

def user_home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request,'user_home.html')

def Logout(request):
    logout(request)
    return redirect('login')


def contact_us(request):
    error=""
    if request.method=="POST":
        f=request.POST['fname']
        m = request.POST['mobile']
        e = request.POST['email']
        c = request.POST['comment']
        try:
            Contact.objects.create(full_name=f,email=e,mobile=m,comment=c)
            error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request,'contact_us.html',d)

def view_contact(request):
    if not request.user.is_authenticated:
        return redirect('login')
    data=Contact.objects.all()
    data2=Feedback.objects.all()
    d={'data':data,'data2':data2}
    return render(request,'view_contact.html',d)

def delete_contact(request,id):
    data=Contact.objects.get(id=id)
    data.delete()
    return redirect('view_contact')

def feedback(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error = ""
    user=request.user
    data=Signup.objects.get(user=user)
    if request.method == "POST":
        n = request.POST['fname']
        m = request.POST['mobile']
        e = request.POST['email']
        f = request.POST['feedback']
        try:
            Feedback.objects.create(full_name=n, email=e, mobile=m, feedback=f)
            error = "no"
        except:
            error = "yes"
    d = {'error': error,'data':data}
    return render(request,'feedback.html',d)


def delete_feedback(request,id):
    data = Feedback.objects.get(id=id)
    data.delete()
    return redirect('view_contact')


def view_room_user(request):
    if not request.user.is_authenticated:
        return redirect('login')
    data=Room.objects.all()
    d={'data':data}
    return render(request,'view_room_user.html',d)

def add_room(request):
    if not request.user.is_staff:
        return redirect('login')
    error=""
    if request.method=='POST':
        r=request.POST['roomno']
        p=request.POST['price']
        t = request.POST['rtype']
        i=request.FILES['image']
        s = request.POST['status']
        try:
            Room.objects.create(room_no=r,price=p,r_type=t,r_image=i,status=s)
            error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request,'add_room.html',d)


def view_room_admin(request):
    if not request.user.is_staff:
        return redirect('login')
    data=Room.objects.all()
    d={'data':data}
    return render(request,'view_room_admin.html',d)

def delete_room(request,id):
    if not request.user.is_staff:
        return redirect('login')
    data= Room.objects.get(id=id)
    data.delete()
    return redirect('view_room_admin')

def edit_room(request,id):
    if not request.user.is_staff:
        return redirect('login')
    error=""
    data = Room.objects.get(id=id)

    if request.method=="POST":
        r= request.POST['roomno']
        p= request.POST['price']
        t= request.POST['rtype']
        s= request.POST['status']

        data.room_no=r
        data.price=p
        data.r_type=t
        data.status=s
        try:
            i = request.FILES['r_img']
            data.r_image = i
        except:
            pass
        try:
            data.save()
            error="no"
        except:
            error="yes"

    d={'data':data,'error':error}
    return render(request,'edit_room.html',d)


def change_password_user(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error=""
    if request.method=="POST":
        c= request.POST['currentpassword']
        n= request.POST['newpassword']
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error="no"
            else:
                error="not"
        except:
            error="yes"
    d={'error':error}
    return render(request,'change_password_user.html',d)

def reset_password(request):
    error=""
    if request.method=="POST":
        u=request.POST['username']
        n= request.POST['newpassword']
        try:
            u=User.objects.get(id=request.user.id)
            u.set_password(n)
            u.save()
            error="no"
        except:
            error="yes"
    d={'error':error}

    return render(request,'reset_password.html',d)

def forgot_password(request):
    error=""
    if request.method=="POST":
        u= request.POST['usernm']
        u = str(u)
        data=User.objects.all()
        for i in data:
            i=str(i)
            print(i)
            if u == i:
                print('hello')
                return redirect('reset_password')
    d={'error':error}
    return render(request,'forgot_password.html',d)


def change_password_admin(request):
    if not request.user.is_staff:
        return redirect('login')
    error=""
    if request.method=="POST":
        c= request.POST['currentpassword']
        n= request.POST['newpassword']
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error="no"
            else:
                error="not"
        except:
            error="yes"
    d={'error':error}
    return render(request,'change_password_admin.html',d)


def book_room(request,id):
    error=""
    data= Room.objects.get(id=id)
    data2= Signup.objects.get(user=request.user)
    if request.method=="POST":
        f= request.POST['fname']
        l= request.POST['lname']
        fn=f+" "+l
        e= request.POST['email']
        r= request.POST['roomno']
        c= request.POST['contact']
        c1= request.POST['contact2']
        b= request.POST['booking_date']
        d= request.POST['select_days']
        g= request.POST['gender']
        p= request.POST['price']
        pr=int(p)*int(d)
        a= request.POST['address']
        try:
            Booking.objects.create(full_name=fn,email_id=e,room_no=r,mobile1=c,mobile2=c1,booking_date=b,days=d,gender=g,price=pr,address=a,status="Pending")
            error="no"
        except:
            error="yes"
    d={'data':data,'data2': data2,'error':error}
    return render(request,'book_room.html',d)

def my_booking(request):
    data= Booking.objects.all()
    d={'data':data}
    return render(request,'my_booking.html',d)

def cancel_booking(request,id):
    data = Booking.objects.get(id=id)
    data.delete()
    return redirect('my_booking')

def view_booking(request):
    data = Booking.objects.all()
    d= {'data':data}
    return render(request,'view_booking.html',d)

def change_status(request,id):
    error=""
    data = Booking.objects.get(id=id)
    if request.method=='POST':
        s= request.POST['rstatus']
        data.status=s
        try:
            data.save()
            error="no"
        except:
            error="yes"
    d= {'data':data,'error':error}
    return render(request,'change_status.html',d)


def view_user(request):
    data = Signup.objects.all()
    d={'data':data}
    return render(request,'view_user.html',d)

def delete_user(request,id):
    data = User.objects.get(id=id)
    data.delete()
    return redirect('view_user')

def delete_booking(request,id):
    data = Booking.objects.get(id=id)
    data.delete()
    return redirect('view_booking')

def edit_profile(request):
    error=""
    data = request.user
    data2 = Signup.objects.get(user=data)
    if request.method=='POST':
        f= request.POST['fname']
        l= request.POST['lname']
        c= request.POST['contact']
        g= request.POST['gender']
        a= request.POST['address']
        data.first_name=f
        data.last_name=l
        data2.mobile=c
        data2.gender = g
        data2.address = a
        try:
            i = request.FILES['image']
            data2.image = i
            data2.save()
        except:
            pass
        try:
            data.save()
            data2.save()
            error="no"
        except:
            error="yes"

    d= {'data':data,'data2':data2,'error':error}
    return render(request,'edit_profile.html',d)


def search(request):
    n= request.POST['name']
    data = Booking.objects.filter(full_name__icontains=n)
    d= {'data':data}
    return render(request,'view_booking.html',d)

