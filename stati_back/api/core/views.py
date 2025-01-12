from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UploadedFileSerializer
from .models import UploadedFile

# Create your views here.

#Le viewsets.ModelViewSetfournit des méthodes pour gérer les opérations CRUD par défaut.
#Il nous suffit de spécifier la classe du sérialiseur et le queryset.


from rest_framework.decorators import action
from rest_framework.response import Response
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import base64
from io import BytesIO

class UploadedFileViewSet(viewsets.ModelViewSet):
    serializer_class = UploadedFileSerializer
    queryset = UploadedFile.objects.all()

    # Action pour prévisualiser les 10 premières lignes
    @action(detail=True, methods=['get'])
    def preview(self, request, pk=None):
        try:
            uploaded_file = self.get_object()
            file_path = uploaded_file.file.path
            df = pd.read_csv(file_path)
            preview_data = df.head(10).to_dict(orient='records')  # Afficher les 10 premières lignes
            return Response({"preview": preview_data}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

    # Action pour récupérer les colonnes pour les afficher dans la liste déroulante
    @action(detail=True, methods=['get'])
    def columns(self, request, pk=None):
        try:
            uploaded_file = self.get_object()
            df = pd.read_csv(uploaded_file.file.path)
            columns = df.columns.tolist()
            return Response({'columns': columns})
        except UploadedFile.DoesNotExist:
            return Response({'error': 'File not found'}, status=404)

    # Action pour récupérer une colonne spécifique
    @action(detail=True, methods=['get'])
    def column(self, request, pk=None):
        try:
            uploaded_file = self.get_object()
            df = pd.read_csv(uploaded_file.file.path)

            column_name = request.query_params.get('column_name')
            if column_name is None:
                return Response({'error': 'Veuillez fournir un nom de colonne.'}, status=400)

            if column_name not in df.columns:
                return Response({'error': f'La colonne "{column_name}" n\'existe pas.'}, status=400)

            column_data = df[column_name].tolist()
            return Response({'column': column_data})

        except UploadedFile.DoesNotExist:
            return Response({'error': 'Fichier non trouvé'}, status=404)

 # Action pour récupérer les statistiques de la colonne spécifique
    @action(detail=True, methods=['get'])
    def column_stats(self, request, pk=None):
        try:
            uploaded_file = self.get_object()
            df = pd.read_csv(uploaded_file.file.path)

            column_name = request.query_params.get('column_name')
            if column_name is None:
                return Response({'error': 'Veuillez fournir un nom de colonne.'}, status=400)

            if column_name not in df.columns:
                return Response({'error': f'La colonne "{column_name}" n\'existe pas.'}, status=400)

            # Vérifier si la colonne est numérique
            if not pd.api.types.is_numeric_dtype(df[column_name]):
                return Response({'error': f'La colonne "{column_name}" n\'est pas numérique.'}, status=400)

            # Calcul des statistiques descriptives
            stats = df[column_name].describe().to_dict()

            return Response({'column_stats': stats})

        except UploadedFile.DoesNotExist:
            return Response({'error': 'Fichier non trouvé'}, status=404)
    


    # Action pour récupérer une ligne spécifique d'un fichier CSV
    @action(detail=False, methods=['get'])
    def row(self, request):
        try:
            # Récupérer l'ID du fichier depuis les paramètres de requête
            file_id = request.query_params.get('file_id')
            if file_id is None:
                return Response({'error': 'Veuillez fournir un ID de fichier.'}, status=400)

            # Récupérer le fichier correspondant
            try:
                uploaded_file = UploadedFile.objects.get(id=file_id)
            except UploadedFile.DoesNotExist:
                return Response({'error': 'Fichier non trouvé.'}, status=404)

            # Lire le fichier CSV
            df = pd.read_csv(uploaded_file.file.path)

            # Récupérer l'indice de ligne depuis les paramètres de requête
            row_index = request.query_params.get('row_index')
            if row_index is None:
                return Response({'error': 'Veuillez fournir un indice de ligne.'}, status=400)

            try:
                row_index = int(row_index)  # Convertir en entier
            except ValueError:
                return Response({'error': 'L\'indice de ligne doit être un entier.'}, status=400)

            # Vérifier si l'indice est dans les limites
            if row_index < 0 or row_index >= len(df):
                return Response({'error': f'L\'indice "{row_index}" est hors des limites.'}, status=400)

            # Récupérer la ligne correspondante
            row_data = df.iloc[row_index].to_dict()
            return Response({'row': row_data})

        except Exception as e:
            return Response({'error': f'Erreur lors du traitement: {str(e)}'}, status=500)

# Fonction utilitaire pour convertir les graphiques en images encodées en base64
    def get_graph_base64(self):
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        buffer.close()
        plt.clf()
        return image_base64

    # Action pour générer différents types de graphiques
    @action(detail=True, methods=['get'])
    def plot(self, request, pk=None):
        try:
            uploaded_file = self.get_object()
            file_path = uploaded_file.file.path
            df = pd.read_csv(file_path)

            # Récupérer les paramètres de la requête
            chart_type = request.query_params.get('chart_type', 'scatterplot')
            x_column = request.query_params.get('x')
            y_column = request.query_params.get('y')

            # Vérifier si les colonnes spécifiées existent dans le DataFrame
            if x_column and x_column not in df.columns:
                return Response({"error": f"La colonne '{x_column}' n'existe pas."}, status=400)
            if y_column and y_column not in df.columns:
                return Response({"error": f"La colonne '{y_column}' n'existe pas."}, status=400)

            # Générer le graphique en fonction du type
            plt.figure(figsize=(10, 6))

            if chart_type == 'histogram':
                sns.histplot(df[x_column], kde=True)
            elif chart_type == 'barplot':
                sns.barplot(x=x_column, y=y_column, data=df)
            elif chart_type == 'scatterplot':
                sns.scatterplot(x=x_column, y=y_column, data=df)
            elif chart_type == 'boxplot':
                sns.boxplot(x=x_column, y=y_column, data=df)
            elif chart_type == 'violinplot':
                sns.violinplot(x=x_column, y=y_column, data=df)
            elif chart_type == 'lineplot':
                sns.lineplot(x=x_column, y=y_column, data=df)
            elif chart_type == 'heatmap':
                sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
            elif chart_type == 'countplot':
                sns.countplot(x=x_column, data=df)
            elif chart_type == 'kdeplot':
                sns.kdeplot(x=df[x_column], y=df[y_column], fill=True)
            else:
                return Response({"error": "Type de graphique non pris en charge."}, status=400)

            # Retourner le graphique en base64
            image_base64 = self.get_graph_base64()
            return Response({"chart": image_base64}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=400)
