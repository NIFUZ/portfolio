from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User,Group


# Create your views here.
from myapp.models import *


def adminhome(request):
    return render(request, 'admin/admin index.html')

def view_feedback(request):
    return render(request, 'admin/feedback.html')

def loginget(request):
    return render(request,'login index.html')

def loginpost(request):
    uname=request.POST['username']
    upass=request.POST['password']
    user=authenticate(request,username=uname,password=upass)

    if user is not None :
        if user.groups.filter(name="Admin").exists():
            login(request,user)

            return redirect('/myapp/adminhome/')
        elif user.groups.filter(name="Staff").exists():
            login(request,user)
            a=staff_table.objects.get(LOGIN_id=user.id)
            request.session['name']=a.name
            request.session['img']=str(a.photo)
            request.session['place']=a.place
            request.session['Email']=a.email
            request.session['phone'] = a.phone
            request.session['qualification'] = a.qualification
            request.session['experience'] = a.experience
            return redirect('/myapp/staffhome/')
        else:
            return redirect('/myapp/loginget/')

    else:
        return redirect('/myapp/loginget/')



def sendreply(request):
    return render(request, 'admin/reply.html')


def sendreplypost(request):
    ureply=request.POST['reply']
    return redirect('/')

def verifyplayschool(request):
    ja=playschool_table.objects.all()
    return render(request, 'admin/verifyplayschool.html',{'tata':ja})

def acceptplayschool(request,id):
    a=playschool_table.objects.filter(id=id).update(status='accepted')
    messages.success(request,'playschool Approved')
    return redirect('/myapp/verify_get/')

def rejectplayschool(request,id):
    a=playschool_table.objects.filter(id=id).update(status='reject')
    messages.success(request,'playschool reject')
    return redirect('/myapp/verify_get/')


def verifystaff(request):
    da=staff_table.objects.all()
    return render(request, 'admin/verifystaff.html',{'data':da})

def acceptstaff(request,id):
    a=staff_table.objects.filter(id=id).update(status='accepted')
    messages.success(request,'staff Approved')
    return redirect('/myapp/staff_get/')

def rejectstaff(request,id):
    a=staff_table.objects.filter(id=id).update(status='reject')
    messages.success(request,'staff reject')
    return redirect('/myapp/staff_get/')


def viewcomplaint(request):
    return render(request, 'admin/viewcomplaint.html')

def staffhome(request):
    playschool=playschool_table.objects.all()
    camera=camera_table.objects.all()
    return render(request, 'staff/panel.html',{"ply":playschool,"camera":camera})

def chat_with_parent(request):
    return render(request, 'staff/chat_with_parent.html')

def child_monitoring(request):
    return render(request, 'staff/child_monitoring.html')


def manage_camera_add(request):
    return render(request, 'staff/manage_camera_add.html')

def manage_camera_addpost(request):
    camerano = request.POST['camerano']
    camerana = request.POST['camerana']
    l=playschool_table.objects.get(staffid__LOGIN__id=request.user.id)
    fd=camera_table()
    fd.camera_number=camerano
    fd.camera_name=camerana
    fd.playschool_id=l
    fd.date=datetime.now()
    fd.save()
    return redirect('/myapp/staffhome/')

#
def manage_camera_view(request):
    ca=camera_table.objects.filter(playschool_id__staffid__LOGIN_id=request.user.id)
    print(ca,'hhhh')
    return render(request, 'staff/panel.html',{"camera":ca})


#
#
# def manage_camera_view(request):
#     ca = camera_table.objects.filter(playschool_id__staffid__LOGIN_id=request.user.id)
#     ply = playschool_table.objects.filter(staffid__LOGIN_id=request.user.id)
#
#     return render(request, "staff/panel.html", {
#         "camera": ca,
#         "ply": ply,
#     })

def manage_playschool_add(request):
    return render(request, 'staff/manage_playschool_add.html')

def manage_playschool_addpost(request):
    mname= request.POST['mname']
    mplace = request.POST['mplace']
    mpost = request.POST['mpost']
    mpincode = request.POST['mpincode']
    mimage = request.FILES['mimage']
    mmail = request.POST['mmail']
    mphone = request.POST['mphone']
    mwebsite = request.POST['mwebsite']
    mproof = request.FILES['mproof']
    mlatitude = request.POST['mlatitude']
    mlongitude = request.POST['mlongitude']
    ob=playschool_table.objects.filter(staffid__LOGIN__id=request.user.id)
    if ob is None:
        mo=playschool_table()
        mo.name = mname
        mo.place = mplace
        mo.pincode = mpincode
        mo.email = mmail
        mo.proof = mproof
        mo.phone = mphone
        mo.post = mpost
        mo.latitude =mlatitude
        mo.longitude =mlongitude
        mo.image=mimage
        mo.website=mwebsite
        mo.status='pending'
        mo.staffid=staff_table.objects.get(LOGIN_id=request.user.id)
        mo.save()
        return redirect('/myapp/staffhome/')
    else:
        return HttpResponse('''<script>alert("already 1 playschool exists;");window.location="/myapp/staffhome/"</script>''')

def manage_playschool_update(request):
    return render(request, 'staff/manage_playschool_update.html')

def manage_playschool_updatepost(request):
    zname = request.POST['zname']
    zplace = request.POST['zplace']
    zpost = request.POST['zpost']
    zpincode = request.POST['zpincode']
    zimage = request.POST['zimage']
    zmail = request.POST['zmail']
    zphone = request.POST['zphone']
    zwebsite = request.POST['zwebsite']
    zproof = request.POST['zproof']
    zlatitude = request.POST['zlatitude']
    zlongitude = request.POST['zlongitude']
    return redirect(request, '/')

def playschool_delete(request,id):
    dl=playschool_table.objects.get(id=id)
    dl.delete()
    return redirect('/myapp/staffhome/')



def manage_playschool_view(request):
    return render(request, 'staff/manage_playschool_view.html')

def register(request):
    return render(request, 'staff/register.html')

def registerpost(request):
    sname=request.POST['sname']
    smail=request.POST['smail']
    sphone=request.POST['sphone']
    splace=request.POST['splace']
    spincode=request.POST['spincode']
    squalification=request.POST['squalification']
    sphoto=request.FILES['sphoto']
    sproof=request.FILES['sproof']
    susername=request.POST['susername']
    SEXPERIENCE=request.POST['SEXPERIENCE']
    spass=request.POST['spass']

    lg=User.objects.create_user(username=susername,password=spass)
    lg.save()
    lg.groups.add(Group.objects.get(name="Staff"))


    obj=staff_table()
    obj.name=sname
    obj.place=splace
    obj.pincode=spincode
    obj.email=smail
    obj.experience=SEXPERIENCE
    obj.id_proof=sproof
    obj.phone=sphone
    obj.qualification=squalification
    obj.photo=sphoto
    obj.LOGIN=lg
    obj.save()

    return redirect('/myapp/login_get/')

def update_profile(request):
    bn = staff_table.objects.get(LOGIN=request.user.id)
    return render(request,'staff/update_profile.html',{'data':bn})

def update_profilepost(request):
    aname=request.POST['aname']
    amail=request.POST['amail']
    aphone=request.POST['aphone']
    aplace=request.POST['aplace']
    apincode=request.POST['apincode']
    aqualification=request.POST['aqualification']
    aphoto=request.FILES['aphoto']
    aproof=request.FILES['aproof']

    qa=staff_table.objects.get(LOGIN=request.user.id)
    qa.name = aname
    qa.place = aplace
    qa.pincode = apincode
    qa.email = amail
    qa.id_proof = aproof
    qa.phone = aphone
    qa.qualification = aqualification
    qa.photo = aphoto
    qa.save()
    return redirect('/myapp/view_profile/')


def view_attendence(request):
    return render(request, 'staff/view_attendence.html')

def view_request_and_verify(request):
    return render(request, 'staff/view_request_and_verify.html')

def view_profile(request):
    vr=staff_table.objects.get(LOGIN_id=request.user.id)
    return render(request, 'staff/panel.html',{'data':vr})
