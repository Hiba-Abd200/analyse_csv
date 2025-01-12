<template>
  <div>
    <Header />
  </div>
  <div class="main-container">
    <!-- Menu -->
    <Menu class="menu" />

    <!-- Contenu principal -->
    <div class="content">
      <div>
        <div v-if="error" class="error">{{ error }}</div>

        <!-- Tableau -->
        <el-table v-if="previewData.length" :data="previewData" border  style="width: 100%">
          <el-table-column
            v-for="(header, index) in Object.keys(previewData[0])"
            :key="index"
            :label="header"
            :prop="header"
          />
        </el-table>

        <p v-else-if="loading">Chargement des données...</p>
      </div>
      
    </div>
  </div>
</template>

<script>
import { ElTable, ElTableColumn } from 'element-plus';

export default {
  components: {
    ElTable,
    ElTableColumn,
  },
  data() {
    return {
      previewData: [],
      error: null,
      loading: true,
    };
  },
  async mounted() {
    const fileId = localStorage.getItem('fileId'); // Récupérer l'ID depuis localStorage
    if (!fileId) {
      this.error = 'Aucun fichier trouvé';
      this.loading = false;
      return;
    }

    const apiUrl = `http://127.0.0.1:8000/api/files/${fileId}/preview/`;

    try {
      const response = await fetch(apiUrl);

      if (!response.ok) {
        throw new Error(`Erreur HTTP : ${response.status}`);
      }

      const data = await response.json();
      this.previewData = data.preview || [];
    } catch (error) {
      this.error = error.message;
    } finally {
      this.loading = false;
    }
  },
};
</script>

<style scoped>
.main-container {
  display: flex;
  min-height: 100vh;
}

.menu {
  flex-shrink: 0;
  width: 200px;
}

.content {
  flex-grow: 1;
  padding: 20px;
}

.error {
  color: red;
}
</style>
