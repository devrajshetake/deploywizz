from django.shortcuts import render, HttpResponse
from .VMUtils import VMUtils
from .models import VirtualMachine

# Create your views here.
def test_view(request):
    my_vm = VirtualMachine.objects.first()

    util = VMUtils(my_vm)

    return HttpResponse("OK")