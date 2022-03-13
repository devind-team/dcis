<template lang="pug">
  bread-crumbs(:items="bc")
    v-card
      v-card-title {{ period.name }}
        v-spacer
        v-spacer
        v-dialog(v-model="active" width="600")
          template(#activator="{ on }")
            v-btn(v-on="on" color="primary") Создать новый документ
          v-card
            v-card-title Создать новый документ
            v-card-text
              v-text-field(v-model="comment" label="Комментарий")
            v-card-actions
              v-btn(@click="active = false") Закрыть
              v-spacer
              v-btn(@click="AddDocumentMutate({ comment: comment, periodId: $route.params.periodId })" color="primary") Создать
      v-card-subtitle {{ period.project.name }}
      v-card-text
        v-data-table(:headers="headers" :items="period.documents" disable-pagination hide-default-footer)
          template(#item.version="{ item }")
            nuxt-link(
              :to="localePath({ name: 'dcis-documents-documentId', params: { documentId: item.id } })"
            ) Версия {{ item.version }}
          template(#item.actions="{ item }")
            apollo-mutation(
              v-slot="{ mutate, loading, error }"
              :mutation="require('~/gql/dcis/mutations/document/unload_document.graphql')"
              :variables="{ documentId: item.id }"
              tag
              @done="unloadDocumentDone"
            )
              v-icon(@click="mutate") mdi-download
</template>

<script lang="ts">
import { useMutation } from '@vue/apollo-composable'
import { DataTableHeader } from 'vuetify'
import type { ComputedRef, PropType, Ref } from '#app'
import { computed, defineComponent, ref, useNuxt2Meta, inject } from '#app'
import { useI18n } from '~/composables'
import { BreadCrumbsItem } from '~/types/devind'
import {
  AddDocumentMutation,
  AddDocumentMutationVariables,
  PeriodType,
  UnloadDocumentMutationPayload
} from '~/types/graphql'
import addDocumentMutation from '~/gql/dcis/mutations/document/add_document.graphql'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'

export type UnloadDocumentResultType = { data: { unloadDocument: UnloadDocumentMutationPayload } }

export default defineComponent({
  components: { BreadCrumbs },
  middleware: 'auth',
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true }
  },
  setup (props) {
    const { localePath } = useI18n()
    useNuxt2Meta({ title: props.period.name })

    const active: Ref<boolean> = ref<boolean>(false)
    const comment: Ref<string> = ref<string>('')

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      { text: 'Документы', to: localePath({ name: 'dcis-periods-periodId-document' }), exact: true }
    ]))

    const periodUpdate: any = inject('periodUpdate')

    const { mutate: addDocumentMutate } = useMutation<AddDocumentMutation, AddDocumentMutationVariables>(addDocumentMutation, {
      update: (cache, result) => periodUpdate(cache, result, (dataCache, { data: { addDocument: { success, document } } }) => {
        if (success) {
          active.value = false
          dataCache.period.documents = [document, ...dataCache.period.documents]
        }
        return dataCache
      })
    })
    const unloadDocumentDone = ({ data: { unloadDocument: result } }: UnloadDocumentResultType): void => {
      if (result.success) {
        window.open(`/${result.src!}`)
      }
    }
    const headers: DataTableHeader[] = [
      { text: 'Версия', value: 'version' },
      { text: 'Комментарий', value: 'comment' },
      { text: 'Дата создания', value: 'createdAt' },
      { text: 'Действия', value: 'actions', sortable: false }
    ]

    return { active, comment, bc, headers, addDocumentMutate, unloadDocumentDone }
  }
})
</script>
