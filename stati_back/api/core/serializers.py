# Ce fichier est dédié pour convertir les données des modèles Django en JSON, 
# Car le frontend (Nuxt.js) communiquera avec le backend via des appels API.
# Les sérialiseurs sont essentiels pour structurer et envoyer les données dans un format compréhensible pour le frontend.


from rest_framework import serializers
from .models import UploadedFile

# Sérialiseur pour le modèle UploadedFile
class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['id', 'file', 'uploaded_at']