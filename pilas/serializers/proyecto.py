from rest_framework import serializers
from pilas.models.proyecto import Proyecto
#from rest_framework_json_api.relations import ResourceRelatedField


class ProyectoSerializer(serializers.ModelSerializer):

    #pais = ResourceRelatedField(many=False, read_only=True)
    #participaciones = ResourceRelatedField(many=True, read_only=True)

    class Meta:
        model = Proyecto
        fields = ('id', 'nombre') # 'pais'

    #included_serializers = {
    #    'participaciones': 'pilas.serializers.participacion.ParticipacionSerializer',
    #    'pais': 'pilas.serializers.pais.PaisSerializer'
    #}

    #class JSONAPIMeta:
    #    included_resources = ['participaciones', 'pais']
