from rest_framework import serializers
from pilas.models.perfil import Perfil
#from rest_framework_json_api.relations import ResourceRelatedField


class PerfilSerializer(serializers.ModelSerializer):

    #pais = ResourceRelatedField(many=False, read_only=True)
    #participaciones = ResourceRelatedField(many=True, read_only=True)

    class Meta:
        model = Perfil
        fields = ('id', 'nombre') # 'pais'

    #included_serializers = {
    #    'participaciones': 'pilas.serializers.participacion.ParticipacionSerializer',
    #    'pais': 'pilas.serializers.pais.PaisSerializer'
    #}

    #class JSONAPIMeta:
    #    included_resources = ['participaciones', 'pais']
