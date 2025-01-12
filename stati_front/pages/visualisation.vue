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
        <div class="p-6 max-w-xl mx-auto bg-white rounded-lg shadow-md space-y-6">
          <h1 class="text-2xl font-bold text-gray-700">Consulter les Données</h1>

          <!-- Choix entre Ligne et Colonne -->
          <el-radio-group v-model="choice" size="large">
            <el-radio-button :value="'line'">Ligne</el-radio-button>
            <el-radio-button :value="'column'">Colonne</el-radio-button>
          </el-radio-group>

          <!-- Input pour l'index de ligne -->
          <div v-if="choice === 'line'" class="space-y-4">
            <el-input v-model="lineIndex" type="number" placeholder="Entrer l'index de la ligne" size="large" />
            <el-button type="primary" size="large" @click="fetchLine">
              Consulter Ligne
            </el-button>
          </div>

          <!-- Sélection pour les colonnes -->
          <div v-if="choice === 'column'" class="space-y-4">
            <el-select v-model="selectedColumn" placeholder="Sélectionner une colonne" size="large" filterable>
              <el-option v-for="column in columns" :key="column" :label="column" :value="column" />
            </el-select>
            <el-button type="primary" size="large" @click="fetchColumn">
              Consulter Colonne
            </el-button>

            <!-- Sélection pour les types de graphiques -->
            <el-select v-model="selectedChartType" placeholder="Sélectionner un type de graphique" size="large" class="mt-4">
              <el-option v-for="type in chartTypes" :key="type.value" :label="type.label" :value="type.value" />
            </el-select>
            <el-button type="primary" size="large" @click="fetchChart" class="mt-2">
              Générer Graphique
            </el-button>
          </div>

          <!-- Résultats de la ligne ou de la colonne -->
          <div v-if="result" class="p-4 bg-gray-50 rounded-lg shadow">
            <h2 class="text-lg font-semibold text-gray-600">Résultats :</h2>
            <pre class="text-sm text-gray-800">{{ result }}</pre>
          </div>
        </div>
      </div>
    </div>

    <!-- Nouvelle section pour afficher les graphes dans un carousel -->
    <div v-if="chart" class="p-6 w-full max-w-4xl mx-auto bg-white rounded-lg shadow-md space-y-6">
      <h2 class="text-lg font-semibold text-gray-600">Graphique :</h2>
      <el-carousel :interval="5000" arrow="always" type="card" height="400px">
        <el-carousel-item>
          <div class="flex items-center justify-center h-full bg-gray-100 rounded-lg p-4">
            <img :src="'data:image/png;base64,' + chart" alt="Graphique" class="w-full h-auto" />
          </div>
        </el-carousel-item>
      </el-carousel>
    </div>

    <!-- Si aucun graphique n'est disponible -->
    <div v-if="!chart" class="p-4 bg-gray-50 rounded-lg shadow">
      <h2 class="text-lg font-semibold text-gray-600">Aucun graphique disponible</h2>
      <p class="text-sm text-gray-800">Veuillez sélectionner une colonne et un type de graphique pour générer un visuel.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const choice = ref('line')
const lineIndex = ref(null)
const selectedColumn = ref(null)
const columns = ref([])
const result = ref(null)
const chart = ref(null)  // Variable pour stocker le graphique
const selectedChartType = ref(null)
const fileId = ref(null)
const chartTypes = ref([
  { label: 'Histogramme', value: 'histogram' },
  { label: 'Barplot', value: 'barplot' },
  { label: 'Scatterplot', value: 'scatterplot' },
  { label: 'Boxplot', value: 'boxplot' },
  { label: 'Violinplot', value: 'violinplot' },
  { label: 'Lineplot', value: 'lineplot' },
  { label: 'Heatmap', value: 'heatmap' },
  { label: 'Countplot', value: 'countplot' },
  { label: 'KDE Plot', value: 'kdeplot' },
])

onMounted(async () => {
  fileId.value = localStorage.getItem('fileId')
  if (!fileId.value) {
    alert('Aucun fichier trouvé dans le stockage local.')
    return
  }

  try {
    const response = await fetch(`http://127.0.0.1:8000/api/files/${fileId.value}/columns/`)
    const data = await response.json()
    columns.value = data.columns || []
  } catch (error) {
    console.error('Erreur lors du chargement des colonnes:', error)
  }
})

const fetchLine = async () => {
  if (lineIndex.value === null) {
    alert('Veuillez entrer un index de ligne.')
    return
  }
  try {
    const response = await fetch(
      `http://localhost:8000/api/files/row/?file_id=${fileId.value}&row_index=${lineIndex.value}`
    )
    const data = await response.json()
    result.value = data.row || 'Aucune donnée trouvée.'
  } catch (error) {
    console.error('Erreur lors de la récupération de la ligne:', error)
  }
}

const fetchColumn = async () => {
  if (!selectedColumn.value) {
    alert('Veuillez sélectionner une colonne.')
    return
  }
  try {
    const response = await fetch(
      `http://localhost:8000/api/files/${fileId.value}/column/?column_name=${selectedColumn.value}`
    )
    const data = await response.json()
    result.value = data.column || 'Aucune donnée trouvée.'
  } catch (error) {
    console.error('Erreur lors de la récupération de la colonne:', error)
  }
}

const fetchChart = async () => {
  if (!selectedColumn.value || !selectedChartType.value) {
    alert('Veuillez sélectionner une colonne et un type de graphique.')
    return
  }
  try {
    const response = await fetch(
      `http://localhost:8000/api/files/${fileId.value}/plot/?chart_type=${selectedChartType.value}&x=${selectedColumn.value}`
    )
    const data = await response.json()
    chart.value = data.chart || null
  } catch (error) {
    console.error('Erreur lors de la récupération du graphique:', error)
  }
}
</script>

<style scoped>
.menu {
  flex-shrink: 0;
  width: 200px;
}

.main-container {
  display: flex;
  min-height: 100vh;
}
</style>
