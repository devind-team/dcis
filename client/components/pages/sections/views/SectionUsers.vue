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
import { Vue, Component, Prop } from 'vue-property-decorator'
import { SectionUsersType } from '~/types/graphql'

@Component<SectionUsers>({})
export default class SectionUsers extends Vue {
  @Prop() section!: SectionUsersType
}
</script>
