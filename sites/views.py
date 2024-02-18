from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Site, Deployment
from .serializers import SiteSerializer, DeploymentSerializer

class DeploySiteView(generics.UpdateAPIView):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer

    def put(self, request, *args, **kwargs):
        site_id = kwargs.get('pk')
        try:
            site = self.get_object()
            site.deploy()
            messages.success(request, f"Site {site.name} deployed successfully.")
            return Response({'detail': f"Site {site.name} deployed successfully."}, status=status.HTTP_200_OK)
        except Site.DoesNotExist:
            messages.error(request, f"Site with id {site_id} does not exist.")
            return Response({'error': f"Site with id {site_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

class SiteListView(generics.ListAPIView):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer

class DeploymentListView(generics.ListCreateAPIView):
    queryset = Deployment.objects.all()
    serializer_class = DeploymentSerializer

class DeploymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Deployment.objects.all()
    serializer_class = DeploymentSerializer
