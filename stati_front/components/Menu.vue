<template>
  <div class="menu-container">
    <el-menu  class="el-menu-vertical-demo" collapse-transition :collapse="false">
      <el-menu-item index="/affichage">
        <NuxtLink to="/affichage">
          <el-icon>
            <ElIconDocument /> 
          </el-icon>
          <span class=" font-medium">Affichage</span>
        </NuxtLink>
      </el-menu-item>
      <el-menu-item index="/analyse">
        <NuxtLink to="/analyse">
          <el-icon>
            <ElIconDataAnalysis />
          </el-icon>
          <span class=" font-medium">Analyse</span>
        </NuxtLink>
      </el-menu-item>
      <el-menu-item index="/visualisation">
        <NuxtLink to="/visualisation">
          <el-icon>
            <ElIconHistogram />
          </el-icon>
          <span class=" font-medium">Visualisation</span>
        </NuxtLink>
      </el-menu-item>
    </el-menu>
    <div class="page-container">
      <NuxtPage /> <!-- Affiche dynamiquement les pages liées -->
    </div>
  </div>
</template>

<script lang="ts" setup>
</script>

<style>
.menu-container {
  display: flex;
}

.el-menu-vertical-demo {
  width: 200px;
  border: none;
}

.page-container {
  flex-grow: 1;
  padding: 20px;
}
</style>
