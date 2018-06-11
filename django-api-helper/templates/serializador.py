from rest_framework import serializers
from aplicacion.models.modelo import Modelo
#from rest_framework_json_api.relations import ResourceRelatedField


class ModeloSerializer(serializers.ModelSerializer):

    #pais = ResourceRelatedField(many=False, read_only=True)
    #participaciones = ResourceRelatedField(many=True, read_only=True)

    class Meta:
        model = Modelo
        fields = ('id', 'nombre') # 'pais'

    #included_serializers = {
    #    'participaciones': 'aplicacion.serializers.participacion.ParticipacionSerializer',
    #    'pais': 'aplicacion.serializers.pais.PaisSerializer'
    #}

    #class JSONAPIMeta:
    #    included_resources = ['participaciones', 'pais']
