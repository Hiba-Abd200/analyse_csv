<template>
  <div class="login-page flex flex-col min-h-screen bg-gray-200">
    <div class="py-20 px-6 text-white bg-opacity-70">
      <h1 class="mb-12 text-5xl text-left font-mono">
        Nouvelle norme<br />
        d'analyse de données
      </h1>
    </div>
    <div class="w-full">
      <el-card class="w-[28rem] p-6 rounded-xl shadow-lg bg-white absolute right-32">
        <h2 class="text-2xl font-bold text-center mb-6">Télécharger un fichier CSV</h2>
        <el-upload ref="uploadRef" class="w-full" drag action="http://localhost:8000/api/files/" :auto-upload="false"
          accept=".csv" :before-upload="beforeUpload" :on-success="handleSuccess" :on-error="handleError">
          <i class="el-icon-upload text-5xl text-blue-500 mb-4"></i>
          <p class="text-base text-gray-600">Glissez-déposez ou cliquez pour télécharger</p>
        </el-upload>

        <!-- Conteneur pour aligner les boutons verticalement -->
        <div class="flex flex-col items-center space-y-4 mt-6">
          <!-- Bouton Télécharger -->
          <el-button class="w-full rounded-full" type="primary" size="large" :loading="loading" @click="triggerUpload">
            <el-icon class="mr-2">
              <ElIconDownload />
            </el-icon>
            Télécharger
          </el-button>

          <!-- Bouton Aller à l'analyse -->
          <el-button v-if="showNavigateButton" class="w-full rounded-full" type="success" size="large"
            @click="navigateToAnalysis">
            <el-icon class="mr-2">
              <ElIconRight />
            </el-icon>
            Aller à l'analyse
          </el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>


<script lang="ts">
import { defineComponent, ref } from 'vue';
import { ElUpload, ElNotification } from 'element-plus';
import { useRouter } from 'vue-router';

export default defineComponent({
  name: 'UploadCSV',
  setup() {
    const uploadRef = ref<InstanceType<typeof ElUpload> | null>(null);
    const loading = ref(false);
    const showNavigateButton = ref(false);
    const router = useRouter();

    const triggerUpload = () => {
      if (uploadRef.value && typeof uploadRef.value.submit === 'function') {
        loading.value = true;
        uploadRef.value.submit();
      } else {
        console.error("Le composant ElUpload n'a pas été trouvé ou la méthode submit n'existe pas.");
      }
    };

    const beforeUpload = (file: File) => {
      const isCSV = file.type === 'text/csv';
      if (!isCSV) {
        ElNotification({
          title: 'Erreur',
          message: 'Seuls les fichiers CSV sont acceptés.',
          type: 'error',
        });
      }
      return isCSV;
    };

    const handleSuccess = (response: any) => {
      loading.value = false;
      showNavigateButton.value = true;

      // Stocker l'ID du fichier dans localStorage
      const fileId = response.id; // Récupérer l'ID du fichier de la réponse

      localStorage.setItem('fileId', fileId); // Sauvegarder dans localStorage
      ElNotification({
        title: 'Succès',
        message: 'Fichier téléchargé avec succès !',
        type: 'success',
      });
      console.log('Fichier téléchargé avec succès :', response);
    };

    const handleError = (error: any) => {
      loading.value = false;
      ElNotification({
        title: 'Erreur',
        message: 'Erreur lors du téléchargement du fichier.',
        type: 'error',
      });
      console.error('Erreur lors du téléchargement :', error);
    };

    const navigateToAnalysis = () => {
      router.push('/affichage'); // la route de la page d'analyse et visualisation
    };

    return {
      uploadRef,
      triggerUpload,
      beforeUpload,
      handleSuccess,
      handleError,
      loading,
      showNavigateButton,
      navigateToAnalysis,
    };
  },
});
</script>

<style scoped>
.login-page {
  background-image: url('/pics/net.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  height: 100vh;
}

.el-card {
  right: 32rem; /* Ajustez cette valeur pour déplacer vers la gauche */
}
</style>
