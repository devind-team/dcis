<template lang="pug">
  bread-crumbs(:items="breadCrumbs")
    v-card
      v-card-title {{ period.name }}
        template(v-if="hasPerm('dcis.add_document')")
          v-spacer
          v-dialog(v-model="active" width="600")
            template(#activator="{ on }")
              v-btn(v-on="on" color="primary") Создать новый документ
            validation-observer(v-slot="{ handleSubmit, invalid }")
              form(@submit.prevent="handleSubmit(addDocument)")
                v-card
                  v-card-title Создать новый документ
                  v-card-text
                    validation-provider(name="Комментарий" rules="required" v-slot="{ errors, valid }")
                      v-text-field(v-model="comment" :error-messages="errors" :success="valid" label="Комментарий")
                    validation-provider(name="Статус" rules="required" v-slot="{ errors, valid }")
                      v-combobox(v-model="status" :items="statuses" label="Статус" item-text="name" item-value="id")
                  v-card-actions
                    v-btn(@click="active = false") Закрыть
                    v-spacer
                    v-btn(
                      :loading="loading"
                      :disabled="invalid"
                      type="submit"
                      color="primary"
                    ) Создать
      v-card-subtitle {{ period.project.name }}
      v-card-text
        v-data-table(:headers="headers" :items="period.documents" disable-pagination hide-default-footer)
          template(#item.version="{ item }")
            nuxt-link(
              :to="localePath({ name: 'dcis-documents-documentId', params: { documentId: item.id } })"
            ) Версия {{ item.version }}
          template(#item.lastStatus="{ item }")
            template(v-if="item.lastStatus")
              strong {{ item.lastStatus.status.name }}.
              div Назначен: {{ dateTimeHM(item.lastStatus.createdAt) }}
              .font-italic {{ item.lastStatus.comment }}
            template(v-else) Не установлен.
          template(#item.createdAt="{ item }") {{ dateTimeHM(item.createdAt) }}
</template>

<script lang="ts">
import { useMutation } from '@vue/apollo-composable'
import { DataTableHeader } from 'vuetify'
import type { PropType, Ref } from '#app'
import { defineComponent, ref, useNuxt2Meta, inject, useRoute, toRef } from '#app'
import { useCommonQuery, useFilters } from '~/composables'
import type { HasPermissionFnType } from '~/store'
import { useAuthStore } from '~/store'
import { BreadCrumbsItem } from '~/types/devind'
import {
  AddDocumentMutation,
  AddDocumentMutationVariables,
  PeriodType,
  StatusesQuery,
  StatusesQueryVariables,
  StatusType
} from '~/types/graphql'
import statusesQuery from '~/gql/dcis/queries/statuses.graphql'
import addDocumentMutation from '~/gql/dcis/mutations/document/add_document.graphql'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'

export default defineComponent({
  components: { BreadCrumbs },
  middleware: 'auth',
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true }
  },
  setup (props) {
    const authStore = useAuthStore()
    const route = useRoute()
    const { dateTimeHM } = useFilters()
    useNuxt2Meta({ title: props.period.name })

    const hasPerm: Ref<HasPermissionFnType> = toRef(authStore, 'hasPerm')
    const active: Ref<boolean> = ref<boolean>(false)
    const comment: Ref<string> = ref<string>('')
    const status: Ref<StatusType | null> = ref<StatusType | null>(null)

    const { data: statuses } = useCommonQuery<StatusesQuery, StatusesQueryVariables>({
      document: statusesQuery
    })

    const periodUpdate: any = inject('periodUpdate')
    const { mutate, loading } = useMutation<AddDocumentMutation, AddDocumentMutationVariables>(addDocumentMutation, {
      update: (cache, result) => periodUpdate(cache, result, (dataCache, { data: { addDocument: { success, document } } }) => {
        if (success) {
          active.value = false
          dataCache.period.documents = [document, ...dataCache.period.documents]
        }
        return dataCache
      })
    })

    const addDocument = () => {
      mutate({ comment: comment.value, periodId: route.params.periodId, statusId: Number(status.value.id) })
    }

    const headers: DataTableHeader[] = [
      { text: 'Версия', value: 'version' },
      { text: 'Комментарий', value: 'comment' },
      { text: 'Дата создания', value: 'createdAt' },
      { text: 'Статус', value: 'lastStatus' }
    ]

    return { active, comment, status, headers, statuses, addDocument, loading, dateTimeHM, hasPerm }
  }
})
</script>
