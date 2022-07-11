<template lang="pug">
v-data-iterator(:items="section.users" disable-pagination hide-default-footer)
  template(#header)
    v-sheet(v-html="section.text")
  template(#default="{ items }")
    v-list
      v-list-item(v-for="file in items" :key="file.id" :href="`/${file.src}`" target="_blank")
        v-list-item-content
          v-list-item-title {{ file.name }}
          v-list-item-subtitle {{ (file.size / 1024).toFixed(2) }} {{ $t('pages.components.sectionFiles.mb') }}
</template>

<script lang="ts">
import type { PropType } from '#app'
import { defineComponent } from '#app'
import { SectionUsersType } from '~/types/graphql'

export default defineComponent({
  props: {
    section: { type: Object as PropType<SectionUsersType>, required: true }
  }
})
</script>
