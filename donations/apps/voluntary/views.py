from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from donations.apps.voluntary.models import Shelter
from donations.apps.voluntary.models import Voluntary
from donations.apps.voluntary.models import VoluntaryAllocation

from donations.apps.voluntary.serializers import VoluntarySerializer
from donations.apps.voluntary.serializers import ShelterSerializer
from donations.apps.voluntary.serializers import VoluntaryAllocationSerializer
from donations.apps.voluntary.serializers import VoluntaryAllocationModelSerializer

from django.core.exceptions import ValidationError

class VoluntaryView(APIView):
    def get(self, request):
        id = request.query_params.get("id")

        if id:
            try:
                voluntary = Voluntary.objects.get(id=id)
            except ValidationError:
                return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "Invalid UUID"})
            except Voluntary.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "Voluntary not found"})

            serializer = VoluntarySerializer(voluntary)
            return Response(serializer.data)

        voluntaries = Voluntary.objects.all()
        serializer = VoluntarySerializer(voluntaries, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = VoluntarySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, pk):
        voluntary = Voluntary.objects.get(pk=pk)
        serializer = VoluntarySerializer(voluntary, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    def put(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class ShelterView(APIView):
    def get(self, request):
        id = request.query_params.get("id")

        if id:
            try:
                shelter = Shelter.objects.get(id=id)
            except ValidationError:
                return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "Invalid UUID"})
            except Shelter.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "Shelter not found"})

            serializer = ShelterSerializer(shelter)
            return Response(serializer.data)

        shelters = Shelter.objects.all()
        serializer = ShelterSerializer(shelters, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ShelterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, pk):
        shelter = Shelter.objects.get(pk=pk)
        serializer = ShelterSerializer(shelter, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    def put(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class VoluntaryAllocationView(APIView):
    def get(self, request):
        voluntary_allocations = VoluntaryAllocation.objects.all()
        serializer = VoluntaryAllocationModelSerializer(voluntary_allocations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VoluntaryAllocationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, pk):
        voluntary_allocation = VoluntaryAllocation.objects.get(pk=pk)
        serializer = VoluntaryAllocationSerializer(voluntary_allocation, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    def put(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)