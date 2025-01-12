<template>
  <div class="login-page">
    <div class="py-20 px-6 text-white bg-opacity-70">
      <h1 class="mb-12 text-5xl text-left font-mono">
        Nouvelle norme<br />
        d'analyse de données
      </h1>
      <NuxtLink 
        to="/upload" 
        class="inline-block py-4 px-8 bg-teal-900 text-white rounded-xl"
      >
        Browse
      </NuxtLink>

      <!-- Nouveau composant de steps -->
      <el-steps style="max-width: 600px; margin-top: 20px" :active="active" finish-status="success" align-center>
        <el-step title="Step 1" description="Some description" />
        <el-step title="Step 2" description="Some description" />
        <el-step title="Step 3" description="Some description" />
      </el-steps>
      <el-button style="margin-top: 12px" @click="next">Next step</el-button>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const active = ref(0)

const next = () => {
  if (active.value++ > 2) active.value = 0
}
</script>

<style scoped>
.login-page {
  background-image: url('/pics/net.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  height: 100vh;
}
</style>
