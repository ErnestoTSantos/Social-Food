import re
from rest_framework import serializers

from donations.apps.voluntary.models import Address
from donations.apps.voluntary.models import Shelter
from donations.apps.voluntary.models import Voluntary
from donations.apps.voluntary.models import VoluntaryAllocation

from donations.apps.voluntary.utils import Validate
from validate_email import validate_email
from validate_docbr import CPF

validation = Validate()
cpf = CPF()


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"

    def validate(self, data):
        cep = data.get("cep")
        street = data.get("street")
        city = data.get("city")
        neighborhood = data.get("neighborhood")

        errors = {}

        if len(cep) != 8:
            raise serializers.ValidationError("CEP inválido")

        response = validation.verify_cep(cep)
        if not response:
            errors["cep"] = "CEP inválido"

        if street.lower() != response.get("street").lower():
            errors["street"] = "Rua não encontrada."

        if city.lower() != response.get("city").lower():
            errors["city"] = f"Cidade não condiz com o CEP: {cep}."

        if neighborhood.lower() != response.get("neighborhood").lower():
            errors["neighborhood"] = "Bairro não encontrado."

        if errors:
            raise serializers.ValidationError(errors)

        return data


class VoluntarySerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    def create(self, validated_data):
        address_data = validated_data.pop("address")
        address = Address.objects.create(**address_data)

        voluntary = Voluntary.objects.create(address=address, **validated_data)

        return voluntary

    def patch(self, instance, validated_data):
        address_data = validated_data.pop("address")
        address = instance.address
        address, _ = Address.objects.update_or_create(id=address.id, defaults=address_data)

        voluntary, _ = Voluntary.objects.update_or_create(id=instance.id, defaults=validated_data)
        return voluntary

    class Meta:
        model = Voluntary
        fields = "__all__"

    def validate_name(self, name):
        pattern = r"^[a-zA-Z\s]+$"

        if not re.match(pattern, name):
            raise serializers.ValidationError("O nome contém caracteres inválidos.")

        if len(name) < 3:
            raise serializers.ValidationError("Nome muito curto.")

        if " " not in name:
            raise serializers.ValidationError("Digite o nome completo.")

        return name

    def validate_phone(self, phone):
        phone = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")

        if len(phone) != 11 or not phone.isdigit() or Voluntary.objects.filter(phone=phone).exists() and not self.instance:
            raise serializers.ValidationError("Telefone inválido.")

        return phone

    def validate_email(self, email):
        if not validate_email(email) or Voluntary.objects.filter(email=email).exists() and not self.instance:
            raise serializers.ValidationError("Email inválido.")

        return email

    def validate_cpf(self, user_cpf):
        user_cpf = user_cpf.replace(".", "").replace("-", "")

        if not cpf.validate(user_cpf):
            raise serializers.ValidationError("CPF inválido.")

        if Voluntary.objects.filter(cpf=user_cpf).exists() and not self.instance:
            raise serializers.ValidationError("CPF inválido.")

        return user_cpf


class ShelterSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    def create(self, validated_data):
        address_data = validated_data.pop("address")
        address = Address.objects.create(**address_data)

        shelter = Shelter.objects.create(address=address, **validated_data)

        return shelter

    def patch(self, instance, validated_data):
        address_data = validated_data.pop("address")
        address = instance.address
        address, _ = Address.objects.update_or_create(id=address.id, defaults=address_data)

        shelter, _ = Shelter.objects.update_or_create(id=instance.id, defaults=validated_data)

        return shelter


    class Meta:
        model = Shelter
        fields = "__all__"

    def validate_name(self, name):
        if len(name) < 3:
            raise serializers.ValidationError("Nome muito curto. O nome precisa ter mais de 3 caracteres.")

        return name

    def validate_sheltered_number(self, sheltered_number):
        if sheltered_number < 0:
            raise serializers.ValidationError("O número de abrigados não pode ser negativo.")

        return sheltered_number

    def validate_amount_lunchbox(self, amount_lunchbox):
        if amount_lunchbox < 0:
            raise serializers.ValidationError("O número de marmitas não pode ser negativo.")

        return amount_lunchbox


class ShelterValidateSerializer(serializers.Serializer):
    id = serializers.UUIDField()

    def validate_id(self, id):
        shelter = Shelter.objects.get(id=id)

        if not shelter:
            raise serializers.ValidationError("Abrigo não encontrado.")

        return shelter


class VoluntaryValidateSerializer(serializers.Serializer):
    id = serializers.UUIDField()

    def validate_id(self, id):
        voluntary = Voluntary.objects.get(id=id)

        if not voluntary:
            raise serializers.ValidationError("Voluntário não encontrado.")

        return voluntary


class VoluntaryAllocationSerializer(serializers.Serializer):
    voluntary = serializers.UUIDField()
    shelter = serializers.UUIDField()

    def create(self, validated_data):
        voluntary = validated_data.pop("voluntary")
        shelter = validated_data.pop("shelter")

        voluntary_allocation = VoluntaryAllocation.objects.create(voluntary=voluntary, shelter=shelter)

        return voluntary_allocation

    def patch(self, instance, validated_data):
        voluntary_allocation, _ = VoluntaryAllocation.objects.update_or_create(id=instance.id, **validated_data)

        return voluntary_allocation

    def validate_voluntary(self, voluntary):
        if not Voluntary.objects.filter(id=voluntary).exists():
            raise serializers.ValidationError("Voluntário não encontrado.")

        return voluntary

    def validate_shelter(self, shelter):
        if not Shelter.objects.filter(id=shelter).exists():
            raise serializers.ValidationError("Abrigo não encontrado.")

        return shelter

    def validate(self, data):
        voluntary = data.get("voluntary")
        shelter = data.get("shelter")

        if VoluntaryAllocation.objects.filter(voluntary=voluntary, shelter=shelter).exists():
            raise serializers.ValidationError("Voluntário já alocado neste abrigo.")

        return data

class VoluntaryAllocationInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voluntary
        fields = ("id", "name",)


class ShelterAllocationInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shelter
        fields = ("id", "name",)

class VoluntaryAllocationModelSerializer(serializers.ModelSerializer):
    voluntary = VoluntaryAllocationInformationSerializer()
    shelter = ShelterAllocationInformationSerializer()

    class Meta:
        model = VoluntaryAllocation
        fields = "__all__"

