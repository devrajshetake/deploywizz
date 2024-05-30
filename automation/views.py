from django.shortcuts import render, HttpResponse
from .VMUtils import VMUtils
from .JenkinsUtil import JenkinsUtil
from .models import VirtualMachine

# Create your views here.
def test_view(request):
    # my_vm = VirtualMachine.objects.first()

    # util = VMUtils(my_vm)
    # system_info = util.get_system_info()
    # print(system_info)


    my_site = {
        "name" : "test_site"
    }

    util = JenkinsUtil(my_site)
    util.create_job()


    return HttpResponse("OK")


from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import VirtualMachine
from .serializers import VirtualMachineSerializer

@api_view(['GET', 'POST'])
def virtual_machine_view(request):
    if request.method == 'GET':
        virtual_machines = VirtualMachine.objects.all()
        serializer = VirtualMachineSerializer(virtual_machines, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = VirtualMachineSerializer(data=request.data)
        try:
                vm = VirtualMachine.objects.get(public_ip=request.data.get("public_ip"))
        except VirtualMachine.DoesNotExist:
            vm = None


        if vm and vm.cpus:
            return Response(VirtualMachineSerializer(vm).data, status=status.HTTP_200_OK)
        if serializer.is_valid():
            # Ensure the first four fields are compulsory
            if 'user' not in request.data or 'public_ip' not in request.data or 'provider' not in request.data or 'region' not in request.data:
                return Response({"message": "User, public_ip, provider, and region are compulsory fields"}, status=status.HTTP_400_BAD_REQUEST)
            
            
            serializer.save()
            ### Get system Info
            vm = VirtualMachine.objects.get(public_ip=request.data.get("public_ip"))
            util = VMUtils(vm)
            try:
                system_info = util.get_system_info()
            except Exception as e:
                vm.delete()
                return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if system_info:
                vm.cpus = system_info.get('cpus')
                vm.ram = system_info.get('ram')
                vm.memory = system_info.get('memory')
                vm.architecture = system_info.get('architecture')
                vm.save()
            else:
                return Response({"message": "Failed to retrieve system info"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(VirtualMachineSerializer(vm).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def virtual_machine_detail(request, public_ip):
    try:
        virtual_machine = VirtualMachine.objects.get(public_ip=public_ip)
    except VirtualMachine.DoesNotExist:
        return Response({"message": "Virtual machine not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VirtualMachineSerializer(virtual_machine)
        return Response(serializer.data)
random_sites =["", ]
@api_view(['POST'])
def deploy_site(request):
    print("called")
    if 'public_ip' not in request.data or 'git_url' not in request.data:
        return Response({"message": "public_ip and git_url are compulsory fields"}, status=status.HTTP_400_BAD_REQUEST)
    vm = VirtualMachine.objects.get(public_ip=request.data.get("public_ip"))
    git_url = request.data.get("git_url")
    site_name = request.data.get("site_name", "")
    logs = vm.deploy(git_url)
    vm.add_dns_record(site_name, vm.public_ip)

    return Response({"message": "Site deployed successfully", "site_url" : vm.public_ip, "logs" : logs}, status=status.HTTP_200_OK)

    