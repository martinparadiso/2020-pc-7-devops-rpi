from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv46_address

from .models import Device
from .versions import get_versions

import requests

def index(request):
    devices = Device.objects.all()
    context = {
        'devices' : devices
    }
    return render(request, 'dashboard/index.html', context)

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
