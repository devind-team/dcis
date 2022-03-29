<template lang="pug">
  bread-crumbs(:items="breadCrumbs")
    v-card
      v-card-title {{ period.name }}
        template(v-if="hasPerm('dcis.add_document')")
          v-spacer
          add-document(:period-id="$route.params.periodId" :update="addDocumentUpdate")
            template(#activator="{ on }")
              v-btn(v-on="on" color="primary") Создать новый документ
      v-card-subtitle {{ period.project.name }}
      v-card-text
        v-data-table(:headers="headers" :items="period.documents" disable-pagination hide-default-footer)
          template(#item.version="{ item }")
            nuxt-link(
              :to="localePath({ name: 'dcis-documents-documentId', params: { documentId: item.id } })"
            ) Версия {{ item.version }}
          template(#item.lastStatus="{ item }")
            template(v-if="item.lastStatus")
              // document-status(:documentItem="item")
              //  template(#activator="{ on }")
              //    a(v-if="hasPerm('dcis.add_documentstatus')" v-on="on" class="font-weight-bold") {{ item.lastStatus.status.name }}.
              //    strong(v-else) {{ item.lastStatus.status.name }}.
              div Назначен: {{ dateTimeHM(item.lastStatus.createdAt) }}
              .font-italic {{ item.lastStatus.comment }}
          template(#item.createdAt="{ item }") {{ dateTimeHM(item.createdAt) }}
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import { DataTableHeader } from 'vuetify'
import type { PropType } from '#app'
import { defineComponent, useNuxt2Meta, inject, toRef } from '#app'
import { useAuthStore } from '~/store'
import { useFilters } from '~/composables'
import { BreadCrumbsItem } from '~/types/devind'
import { PeriodType } from '~/types/graphql'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import DocumentStatus from '~/components/dcis/documents/DocumentStatus.vue'
import AddDocument, { AddDocumentMutationResultType } from '~/components/dcis/documents/AddDocument.vue'

export default defineComponent({
  components: { AddDocument, BreadCrumbs, DocumentStatus },
  middleware: 'auth',
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true }
  },
  setup (props) {
    const { dateTimeHM } = useFilters()
    useNuxt2Meta({ title: props.period.name })

    const userStore = useAuthStore()
    const hasPerm = toRef(userStore, 'hasPerm')

    const periodUpdate: any = inject('periodUpdate')
    const addDocumentUpdate = (cache: DataProxy, result: AddDocumentMutationResultType) => {
      periodUpdate(cache, result, (dataCache, { data: { addDocument: { success, document } } }: AddDocumentMutationResultType) => {
        if (success) {
          dataCache.period.documents = [document, ...dataCache.period.documents]
        }
        return dataCache
      })
    }

    const headers: DataTableHeader[] = [
      { text: 'Версия', value: 'version' },
      { text: 'Комментарий', value: 'comment' },
      { text: 'Дата создания', value: 'createdAt' },
      { text: 'Статус', value: 'lastStatus' }
    ]

    return {
      headers,
      addDocumentUpdate,
      hasPerm,
      dateTimeHM
    }
  }
})
</script>
