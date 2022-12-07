<template lang="pug">
v-data-table(
  :headers="headers"
  :items="projects"
  :loading="loading"
  disable-pagination
  disable-filtering
  hide-default-footer
)
  template(#item.name="{ item }")
    nuxt-link(
      :to="localePath({ name: 'dcis-projects-projectId-periods', params: { projectId: item.id } })"
    ) {{ item.name }}
  template(#item.createdAt="{ item }") {{ dateTimeHM(item.createdAt) }}
</template>

<script lang="ts">
import { defineComponent, PropType } from '#app'
import { DataTableHeader } from 'vuetify'
import { ProjectType } from '~/types/graphql'
import { useFilters, useI18n } from '~/composables'

export default defineComponent({
  props: {
    projects: { type: Array as PropType<ProjectType[]>, required: true },
    loading: { type: Boolean, required: true }
  },
  setup () {
    const { t } = useI18n()
    const { dateTimeHM } = useFilters()

    const headers = computed<DataTableHeader[]>(() => [
      { text: t('dcis.projects.tableHeaders.name') as string, value: 'name' },
      { text: t('dcis.projects.tableHeaders.description') as string, value: 'description' },
      { text: t('dcis.projects.tableHeaders.createdAt') as string, value: 'createdAt' }
    ])

    return { headers, dateTimeHM }
  }
})
</script>
