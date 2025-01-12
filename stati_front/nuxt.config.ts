// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  css: ['~/assets/css/main.css'],

  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },


  compatibilityDate: '2024-11-01',
  devtools: { enabled: false },
  modules: ['@element-plus/nuxt',
  ]
})