import { defineNuxtPlugin, NuxtAppCompat } from '#app'

export default defineNuxtPlugin((nuxtApp: NuxtAppCompat) => {
  nuxtApp.vueApp.component('ApexChart', () => import('vue-apexcharts'))
})
