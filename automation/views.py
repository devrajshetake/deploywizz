from django.shortcuts import render, HttpResponse
from .VMUtils import VMUtils
from .JenkinsUtil import JenkinsUtil
from .models import VirtualMachine

# Create your views here.
def test_view(request):
    my_vm = VirtualMachine.objects.first()

    util = VMUtils(my_vm)
    system_info = util.get_system_info()
    print(system_info)


    # my_site = {
    #     "name" : "test_site"
    # }

    # util = JenkinsUtil(my_site)
    # util.create_job()


    return HttpResponse("OK")