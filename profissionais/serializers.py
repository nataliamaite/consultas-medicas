from rest_framework import serializers

from .models import Consulta, Profissional


class ProfissionalSerializer(serializers.ModelSerializer):
    nome_social = serializers.CharField(
        max_length=150,
        allow_blank=False,
        error_messages={
            "blank": "O nome social é obrigatório.",
            "required": "O nome social é obrigatório.",
        },
    )

    profissao = serializers.CharField(
        max_length=100,
        allow_blank=False,
        error_messages={
            "blank": "A profissão é obrigatória.",
            "required": "A profissão é obrigatória.",
        },
    )

    endereco = serializers.CharField(
        max_length=255,
        allow_blank=False,
        error_messages={
            "blank": "O endereço é obrigatório.",
            "required": "O endereço é obrigatório.",
        },
    )

    contato = serializers.CharField(
        max_length=100,
        allow_blank=False,
        error_messages={
            "blank": "O contato é obrigatório.",
            "required": "O contato é obrigatório.",
        },
    )

    class Meta:
        model = Profissional
        fields = [
            "id",
            "nome_social",
            "profissao",
            "endereco",
            "contato",
        ]

    def validate_nome_social(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "O nome social é obrigatório."
            )

        return value

    def validate_profissao(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "A profissão é obrigatória."
            )

        return value

    def validate_endereco(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "O endereço é obrigatório."
            )

        return value

    def validate_contato(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "O contato é obrigatório."
            )

        return value


class ConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consulta
        fields = [
            "id",
            "data",
            "profissional",
        ]

    def validate_profissional(self, value):
        if not Profissional.objects.filter(id=value.id).exists():
            raise serializers.ValidationError(
                "O profissional informado não existe."
            )

        return value