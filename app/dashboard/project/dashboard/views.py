from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv46_address
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model

from .models import Device
from .versions import get_versions

import requests

def login_view(request):
    User = get_user_model()
    users = User.objects.all()
    if not users:
        return redirect(reverse('dashboard:register'))

    if request.user.is_authenticated:
        return redirect(reverse('dashboard:index'))

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        next_url = request.POST['next']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect(reverse('dashboard:index'))
        else:
            messages.error(request, 'Wrong username and/or password', extra_tags='danger')
            return redirect(f"/dashboard/login?next={next_url}")

    return render(request, 'dashboard/login.html')

def register_view(request):
    User = get_user_model()
    users = User.objects.all()
    if not users:

        if request.method == 'POST':
            # Proceed to add the user
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['reenter-password']

            if password != password2:
                messages.error(request, 'The passwords must match', extra_tags='danger')
                return render(request, 'dashboard/register.html')
            
            user = User.objects.create_user(username, email, password)

            messages.success(request, f'User {user.username} registered')
            return redirect(reverse("dashboard:index"))
    else:
        return redirect(reverse("dashboard:index"))

    return render(request, 'dashboard/register.html')

@login_required
def log_out(request):
    logout(request)
    messages.success(request, 'Goodbye!')
    return redirect(reverse('dashboard:index'))

@login_required
def index(request):

    devices = Device.objects.all()
    context = {
        'devices' : devices
    }
    return render(request, 'dashboard/index.html', context)

@login_required
def detail(request, pk):
    device = get_object_or_404(Device, pk=pk)
    try:
        reload = request.GET['refresh']
        if reload == 'true':
            try:
                status = requests.get(f"http://{device.ip}:1221/status", timeout=15)
                image = requests.get(f"http://{device.ip}:1221/image", timeout=15)
                tag = requests.get(f"http://{device.ip}:1221/tag", timeout=15)
                device.last_check = timezone.now()
                device.last_status = status.json()['status']
                device.image = image.json()['image']
                device.tag = tag.json()['tag']
                device.save()
                messages.success(request, 'The device information was updated successfully.')
            except requests.exceptions.Timeout:
                messages.error(request, 'The device couldn\'t be reached', extra_tags='danger')
            except requests.exceptions.RequestException as e:
                messages.error(request, str(e), extra_tags='danger')
            except:
                messages.error(request, 'Unknown error', extra_tags='danger')
            finally:
                return redirect(reverse('dashboard:detail', args=(pk,)))
    except:
        pass
    return render(request, 'dashboard/detail.html', { 'device' : device })

@login_required
def add(request):

    # If the request is POST, add the devices
    if request.method == 'POST':
        try:
            name = request.POST['name']
            validate_ipv46_address(request.POST['ip'])
            ip = request.POST['ip']

            new_device = Device.objects.create(name=name,
                                           ip=ip,
                                           date_added=timezone.now())

            return redirect(reverse('dashboard:detail', args=(new_device.id, )))

        except ValidationError as e:
            messages.error(request, e.message, extra_tags='danger')

    return render(request, 'dashboard/add.html')

@login_required
def edit(request, pk):
    device = get_object_or_404(Device, pk=pk)
    
    # If the request is POST, is the submit of th edit
    if request.method == 'POST':
        try:
            new_name = request.POST['name']
            validate_ipv46_address(request.POST['ip'])
            new_ip = request.POST['ip']

            device.name = new_name
            device.ip = new_ip
            device.save()

            return redirect(reverse('dashboard:detail', args=(pk, )))

        except ValidationError as e:
            messages.error(request, e.message, extra_tags='danger')

    return render(request, 'dashboard/edit.html', { 'device' : device })

@login_required
def remove(request, pk):
    device = get_object_or_404(Device, pk=pk)
    name = device.name
    if request.method == 'POST':
        device.delete()
        messages.success(request, f"Device '{name}' removed")
        return redirect(reverse('dashboard:index'))
    else:
        return redirect(reverse('dashboard:detail', args=(pk,)))


@login_required
def change_version(request, pk):
    device = get_object_or_404(Device, pk=pk)

    if request.method == 'POST':
        try:
            new_tag = request.POST['new_version']

            requests.post(f"http://{device.ip}:1221/tag", json={'tag' : new_tag})

            messages.success(request, f"The new version was sent to {device.name}")
            return redirect(f"/dashboard/{pk}?refresh=true")
        except KeyError:
            messages.error(request, 'You must select a tag', extra_tags='danger')
        except:
            messages.error(request, 'The device coudn\t be reached', extra_tags='danger')

    # Get the available version
    versions = get_versions()
    return render(request, 'dashboard/change_version.html', { 'device' : device, 'versions' : versions })
