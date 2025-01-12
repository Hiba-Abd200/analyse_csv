<template>
  <div>
    <nav class="p-6 flex items-center justify-between bg-blue-900">
      <NuxtLink to="/upload" class="text-2xl text-white">Visualytics</NuxtLink>
      <div class="flex items-center space-x-4 ml-auto">
        <NuxtLink to="/upload" class="text-white hover:text-teal-300">Home</NuxtLink>
        <NuxtLink to="/affichage" class="text-white hover:text-teal-300">Browse</NuxtLink>
      </div>
    </nav>
    <slot />
  </div>
</template>