<template lang="pug">
  nuxt-child(:breadCrumbs="bc")
</template>

<script lang="ts">
import { defineComponent, useNuxt2Meta } from '#app'
import { useI18n } from '~/composables'

export default defineComponent({
  setup () {
    const { t, localePath } = useI18n()
    const bc = [
      { text: t('dcis.home'), to: localePath({ name: 'dcis' }), exact: true }
    ]
    useNuxt2Meta({ title: t('dcis.home') as string })
    return { bc }
  }
})
</script>
