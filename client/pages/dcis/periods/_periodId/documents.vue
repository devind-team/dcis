<template lang="pug">
  left-navigator-container(:bread-crumbs="breadCrumbs" @update-drawer="$emit('update-drawer')")
    template(#header) {{ $t('dcis.documents.name') }}
      template(v-if="period.canAddDocument || userPeriodDivision.length")
        v-spacer
        add-document(
          :can-add-any-document="period.canAddDocument"
          :user-divisions="userPeriodDivision"
          :period="period"
          :documents="documents"
          :update="addDocumentUpdate"
        )
          template(#activator="{ on }")
            v-btn(v-on="on" color="primary") {{ $t('dcis.documents.addDocument.buttonText') }}
    template(#subheader) {{ $t('shownOf', { count, totalCount }) }}
    items-data-filter(
      v-if="showDivisionFilter"
      v-model="selectedDocs"
      v-bind="divisionFilterMessages"
      :items="period.divisions.map(x => ({ id: x.id, name: x.name }))"
      :get-name="i => i.name"
      multiple
    )
    v-data-table(:headers="headers" :items="visibleDocs" :loading="loading" disable-pagination hide-default-footer)
      template(#item.version="{ item }")
        nuxt-link(
          :to="localePath({ name: 'dcis-documents-documentId', params: { documentId: item.id } })"
        ) {{ $t('dcis.documents.tableItems.version', { version: item.version }) }}
      template(#item.comment="{ item }")
        template(v-if="item.comment")
          template(v-if="canChangeDocument(item)")
            text-menu(v-slot="{ on }" @update="changeDocumentComment(item, $event)" :value="item.comment")
              a(v-on="on") {{ item.comment }}
          template(v-else) {{ item.comment }}
      template(#item.lastStatus="{ item }")
        template(v-if="item.lastStatus")
          document-statuses(
            :can-add="canChangeDocument(item)"
            :can-delete="canDeleteDocumentStatus(item)"
            :update="update"
            :document="item"
          )
            template(#activator="{ on }")
              a(v-on="on" class="font-weight-bold") {{ item.lastStatus.status.name }}.
          div {{ $t('dcis.documents.tableItems.statusAssigned', { assigned: dateTimeHM(item.lastStatus.createdAt) }) }}
          .font-italic {{ item.lastStatus.comment }}
      template(
        #item.division="{ item }"
      ) {{ item.objectId ? period.divisions.find(x => x.id === item.objectId).name : '-' }}
      template(v-for="dti in ['createdAt', 'updatedAt']" v-slot:[`item.${dti}`]="{ item }") {{ dateTimeHM(item[dti]) }}
</template>

<script lang="ts">
import { useMutation } from '@vue/apollo-composable'
import { DataProxy } from 'apollo-cache'
import { DataTableHeader } from 'vuetify'
import type { PropType } from '#app'
import { computed, defineComponent, useNuxt2Meta, useRoute } from '#app'
import { useAuthStore } from '~/stores'
import { useFilters, useI18n } from '~/composables'
import { useDocumentsQuery } from '~/services/grapqhl/queries/dcis/documents'
import { BreadCrumbsItem } from '~/types/devind'
import {
  ChangeDocumentCommentMutation,
  ChangeDocumentCommentMutationVariables,
  DivisionModelType,
  DocumentType,
  PeriodType
} from '~/types/graphql'
import { FilterMessages } from '~/types/filters'
import changeDocumentCommentMutation from '~/gql/dcis/mutations/document/change_document_comment.graphql'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import ItemsDataFilter from '~/components/common/filters/ItemsDataFilter.vue'
import AddDocument, { AddDocumentMutationResultType } from '~/components/dcis/documents/AddDocument.vue'
import DocumentStatuses from '~/components/dcis/documents/DocumentStatuses.vue'
import TextMenu from '~/components/common/menu/TextMenu.vue'

export default defineComponent({
  components: {
    LeftNavigatorContainer,
    ItemsDataFilter,
    AddDocument,
    DocumentStatuses,
    TextMenu
  },
  middleware: 'auth',
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true }
  },
  setup (props) {
    const { t, tc } = useI18n()
    const route = useRoute()
    const { dateTimeHM } = useFilters()
    useNuxt2Meta({ title: props.period.name })
    const userStore = useAuthStore()

    const userPeriodDivision = computed(() => {
      const userDivisionIds = userStore.user.divisions.map((division: DivisionModelType) => division.id)
      return props.period.divisions.filter((division: DivisionModelType) => userDivisionIds.includes(division.id))
    })

    const canChangeDocument = (document: DocumentType) => {
      return document.canChange || document.user?.id === userStore.user.id
    }
    const canDeleteDocumentStatus = (document: DocumentType) => {
      return document.canChange
    }

    const {
      data: documents,
      loading,
      pagination: { totalCount },
      update,
      addUpdate,
      changeUpdate
    } = useDocumentsQuery(route.params.periodId)

    const addDocumentUpdate = (cache: DataProxy, result: AddDocumentMutationResultType) => {
      if (!result.data.addDocument.errors.length) {
        addUpdate(cache, result, 'document')
      }
    }

    const { mutate: changeDocumentCommentMutate } = useMutation<ChangeDocumentCommentMutation,
      ChangeDocumentCommentMutationVariables>(
        changeDocumentCommentMutation,
        {
          update: (cache, result) => {
            if (!result.errors) {
              changeUpdate(cache, result, 'document')
            }
          }
        }
      )

    const changeDocumentComment = (document: DocumentType, comment: string): void => {
      changeDocumentCommentMutate({ documentId: document.id, comment })
    }

    const divisionFilterMessages = computed<FilterMessages>(() => {
      const filterName = props.period.project.contentType.model === 'department'
        ? 'divisionFilterOrganization'
        : 'divisionFilterDepartment'
      return getFilterMessages(filterName, true)
    })

    const getFilterMessages = (filterName: string, multiple: boolean = false): FilterMessages => {
      return {
        title: t(`dcis.documents.${filterName}.title`) as string,
        noFiltrationMessage: t(`dcis.documents.${filterName}.noFiltrationMessage`) as string,
        multipleMessageFunction: multiple
          ? (name, restLength) =>
              tc(`dcis.documents.${filterName}.multipleMessage`, restLength, { name, restLength }) as string
          : undefined
      }
    }

    const showDivisionFilter = computed<boolean>(() => {
      return props.period.multiple && documents.value && new Set(
        documents.value.map((document: DocumentType) => document.objectId)
      ).size > 1
    })
    const headers = computed<DataTableHeader[]>(() => {
      const result: DataTableHeader[] = showDivisionFilter.value
        ? [{
            text: t(`dcis.documents.tableHeaders.${props.period.project.contentType.model}`) as string,
            value: 'division'
          }]
        : []
      result.push(
        { text: t('dcis.documents.tableHeaders.version') as string, value: 'version' },
        { text: t('dcis.documents.tableHeaders.comment') as string, value: 'comment' },
        { text: t('dcis.documents.tableHeaders.lastStatus') as string, value: 'lastStatus' },
        { text: t('dcis.documents.tableHeaders.createdAt') as string, value: 'createdAt' },
        { text: t('dcis.documents.tableHeaders.updatedAt') as string, value: 'updatedAt' }
      )
      return result
    })

    const selectedDocs = ref<DivisionModelType[]>([])
    const visibleDocs = computed<DocumentType[]>(() => {
      return selectedDocs.value.length > 0
        ? documents.value.filter(x => selectedDocs.value.map(x => x.id).includes(x.objectId))
        : documents.value
    })
    const count = computed(() => {
      return selectedDocs.value.length > 0 ? visibleDocs.value.length : totalCount.value
    })

    return {
      userPeriodDivision,
      canChangeDocument,
      canDeleteDocumentStatus,
      documents,
      loading,
      totalCount,
      update,
      addDocumentUpdate,
      dateTimeHM,
      changeDocumentComment,
      divisionFilterMessages,
      getFilterMessages,
      showDivisionFilter,
      headers,
      selectedDocs,
      visibleDocs,
      count
    }
  }
})
</script>
