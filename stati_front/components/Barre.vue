<template>
  <div class="chart-container">
    <canvas ref="chartCanvas" />
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import Chart from 'chart.js/auto'

const chartCanvas = ref(null)

onMounted(() => {
  const ctx = chartCanvas.value.getContext('2d')
  
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr'],
      datasets: [
        {
          label: 'Ventes',
          data: [12, 19, 3, 5],
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top'
        },
        tooltip: {
          callbacks: {
            label: (tooltipItem) => {
              return `Ventes: ${tooltipItem.raw}`
            }
          }
        }
      }
    }
  })
})
</script>

<style scoped>
.chart-container {
  max-width: 600px;
  margin: auto;
}
</style>
