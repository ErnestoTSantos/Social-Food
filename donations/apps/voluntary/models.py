import uuid
from django.db import models


class Base(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Address(Base):
    cep = models.CharField(max_length=8, verbose_name="CEP")
    street = models.CharField(max_length=100, verbose_name="Rua")
    number = models.IntegerField(verbose_name="Número")
    city = models.CharField(max_length=100, verbose_name="Cidade")
    neighborhood = models.CharField(max_length=100, verbose_name="Bairro")
    complement = models.CharField(max_length=255, null=True, blank=True, verbose_name="Complemento")

    def __str__(self):
        return f"{self.street} -> {self.cep}"

    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"


class Voluntary(Base):
    name = models.CharField(max_length=255, verbose_name="Nome")
    email = models.EmailField(verbose_name="E-mail")
    phone = models.CharField(max_length=20, verbose_name="Telefone")
    cpf = models.CharField(max_length=11, verbose_name="CPF")
    team_type = models.CharField(max_length=100, verbose_name="Tipo de equipe")
    address = models.ForeignKey(Address, on_delete=models.PROTECT, verbose_name="Endereço")

    def __str__(self):
        return f"{self.name} - {self.team_type}"

    class Meta:
        verbose_name = "Voluntário"
        verbose_name_plural = "Voluntários"


class Shelter(Base):
    name = models.CharField(max_length=255, verbose_name="Nome")
    sheltered_number = models.IntegerField(verbose_name="Número de abrigados")
    amount_lunchbox = models.IntegerField(verbose_name="Quantidade de marmitas")
    address = models.ForeignKey(Address, on_delete=models.PROTECT, verbose_name="Endereço")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Abrigo"
        verbose_name_plural = "Abrigos"


class VoluntaryAllocation(Base):
    voluntary = models.ForeignKey(Voluntary, on_delete=models.PROTECT, verbose_name="Voluntário")
    shelter = models.ForeignKey(Shelter, on_delete=models.PROTECT, verbose_name="Abrigo")

    def __str__(self):
        return f"{self.voluntary.name} - {self.shelter.name}"

    class Meta:
        verbose_name = "Alocação de voluntário"
        verbose_name_plural = "Alocações de voluntários"