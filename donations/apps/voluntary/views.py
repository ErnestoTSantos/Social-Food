from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from donations.apps.voluntary.models import Shelter
from donations.apps.voluntary.models import Voluntary
from donations.apps.voluntary.models import Address
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
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_201_CREATED, data={"message": "Voluntary created successfully"})

    def patch(self, request):
        id = request.query_params.get("id")

        try:
            voluntary = Voluntary.objects.get(id=id)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Invalid UUID"})
        except Voluntary.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "Voluntary not found"})

        serializer = VoluntarySerializer(voluntary, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.patch(instance=voluntary, validated_data=serializer.validated_data)

        return Response(status=status.HTTP_200_OK, data={"message": "Voluntary updated successfully"})

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
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_201_CREATED, data={"message": "Shelter created successfully"})

    def patch(self, request):
        id = request.query_params.get("id")

        try:
            shelter = Shelter.objects.get(id=id)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Invalid UUID"})
        except Shelter.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "Shelter not found"})

        serializer = ShelterSerializer(shelter, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.patch(instance=shelter, validated_data=serializer.validated_data)

        return Response(status=status.HTTP_200_OK, data={"message": "Shelter updated successfully"})

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
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request):
        id = request.query_params.get("id")

        try:
            voluntary_allocation = VoluntaryAllocation.objects.get(id=id)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Invalid UUID"})
        except VoluntaryAllocation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "Voluntary allocation not found"})

        serializer = VoluntaryAllocationSerializer(voluntary_allocation, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.patch(instance=voluntary_allocation, validated_data=serializer.validated_data)

        return Response(serializer.data)

    def put(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)