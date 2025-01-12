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
          </div>

          <!-- Résultats de la ligne ou de la colonne -->
          <div v-if="result" class="p-4 bg-gray-50 rounded-lg shadow">
            <h2 class="text-lg font-semibold text-gray-600">Résultats :</h2>
            <table class="min-w-full table-auto">
              <thead>
                <tr>
                  <th class="px-4 py-2 border">Index</th>
                  <th class="px-4 py-2 border">Valeur</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(value, index) in result" :key="index">
                  <td class="px-4 py-2 border">{{ index }}</td>
                  <td class="px-4 py-2 border">{{ value }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Nouvelle section pour afficher les statistiques dans un carousel -->
    <div v-if="columnStats && columnStats !== 'Aucune statistique disponible.'"
      class="p-6 w-full max-w-4xl mx-auto bg-white rounded-lg shadow-md space-y-6">
      <h2 class="text-lg font-semibold text-gray-600">Statistiques de la Colonne :</h2>
      <el-carousel :interval="5000" arrow="always" type="card" height="200px">
        <el-carousel-item v-for="(value, key) in columnStats" :key="key">
          <div class="flex flex-col items-center justify-center h-full bg-gray-100 rounded-lg p-4">
            <h3 class="text-lg font-semibold text-gray-800">{{ translateStat(key) }}</h3>
            <p class="text-xl text-gray-700">{{ value }}</p>
          </div>
        </el-carousel-item>
      </el-carousel>

      <!-- Demande si l'utilisateur veut voir les définitions -->
      <div class="mt-6 bg-gray-50 p-4 rounded-lg shadow">
        <h3 class="text-lg font-semibold text-gray-600">Souhaitez-vous connaître la définition de chaque statistique ?</h3>
        <el-button type="primary" size="large" @click="showDefinitions = !showDefinitions">
          <!-- Icône à l'intérieur du bouton avant le texte -->
          <el-icon class="mr-2">
            <ElIconInfoFilled />
          </el-icon>
          {{ showDefinitions ? 'Cacher les Définitions' : 'Voir les Définitions' }}
        </el-button>
      </div>

      <!-- Définitions des statistiques -->
      <div v-if="showDefinitions" class="mt-6 bg-gray-50 p-4 rounded-lg shadow">
        <div class="space-y-4 mt-4">
          <p><strong>Moyenne :</strong> La moyenne arithmétique, calculée en additionnant toutes les valeurs et en
            divisant par le nombre d'éléments.</p>
          <p><strong>Médiane :</strong> La valeur du milieu lorsque les données sont triées par ordre croissant.</p>
          <p><strong>Q1 :</strong> Le premier quartile, c'est-à-dire la valeur en dessous de laquelle se trouve 25% des
            données.</p>
          <p><strong>Q3 :</strong> Le troisième quartile, c'est-à-dire la valeur en dessous de laquelle se trouve 75%
            des données.</p>
          <p><strong>Mode :</strong> La valeur qui apparaît le plus fréquemment dans les données.</p>
          <p><strong>Minimum :</strong> La plus petite valeur des données.</p>
          <p><strong>Maximum :</strong> La plus grande valeur des données.</p>
          <p><strong>Écart-type :</strong> Une mesure de la dispersion des données par rapport à la moyenne.</p>
          <p><strong>Nombre d'éléments :</strong> Le total des valeurs présentes dans la colonne.</p>
        </div>
      </div>
    </div>

    <!-- Si aucune statistique n'est disponible -->
    <div v-if="columnStats === 'Aucune statistique disponible.'" class="p-4 bg-gray-50 rounded-lg shadow">
      <h2 class="text-lg font-semibold text-gray-600">Statistiques :</h2>
      <p class="text-sm text-gray-800">{{ columnStats }}</p>
    </div>
  </div>
</template>

<script setup>
import { Download } from '@element-plus/icons-vue'
import { ref, onMounted } from 'vue'

const choice = ref('line')
const lineIndex = ref(null)
const selectedColumn = ref(null)
const columns = ref([])
const result = ref(null)
const columnStats = ref(null)  // Nouvelle variable pour stocker les statistiques
const fileId = ref(null)
const showDefinitions = ref(false)  // Nouvelle variable pour contrôler l'affichage des définitions

// Dictionnaire pour traduire les statistiques en anglais vers le français
const statTranslations = {
  mean: 'Moyenne',
  "50%": 'Médiane',
  "75%": 'Q3',
  "25%": 'Q1',
  mode: 'Mode',
  min: 'Minimum',
  max: 'Maximum',
  std: 'Écart-type',
  count: 'Nombre d\'éléments'
}

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

    // Vérifiez si les données sont numériques avant de récupérer les statistiques
    const isNumeric = data.column && data.column.every(value => !isNaN(value));

    if (isNumeric) {
      const statsResponse = await fetch(
        `http://localhost:8000/api/files/${fileId.value}/column_stats/?column_name=${selectedColumn.value}`
      )
      const statsData = await statsResponse.json()
      columnStats.value = statsData.column_stats || 'Aucune statistique disponible.'
    } else {
      columnStats.value = 'Aucune statistique disponible.'; // Réinitialise les statistiques si la colonne n'est pas numérique
    }
  } catch (error) {
    console.error('Erreur lors de la récupération de la colonne:', error)
  }
}

// Fonction pour traduire les statistiques
const translateStat = (key) => {
  return statTranslations[key] || key  // Retourne la traduction ou la clé si non trouvée
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

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 8px;
  text-align: left;
}

th {
  background-color: #f4f4f4;
}
</style>
