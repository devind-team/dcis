<template lang="pug">
bread-crumbs(v-if="period.isAdmin || period.isCurator" :items="breadCrumbs")
  v-card
    v-tabs(grow)
      v-tab {{ $t('dcis.documents.tabs.tabNameDocuments.name') }}
      v-tab {{ $t('dcis.documents.tabs.tabNameNotSupplied.name') }}
      v-tab-item
        v-card(flat)
          v-card-text
            .d-flex
              div {{ $t('shownOf', { count, totalCount }) }}
              template(v-if="period.canAddAnyDivisionDocument || userPeriodDivision.length")
                v-spacer
                add-document-menu(
                  v-slot="{ on, attrs }"
                  :period="period"
                  :documents="documents"
                  :add-document-update="addDocumentUpdate"
                  :add-document-data-update="addDocumentDataUpdate"
                  :user-divisions="userPeriodDivision"
                )
                  v-btn(v-on="on" v-bind="attrs" color="primary") {{ $t('dcis.documents.addDocument.buttonText') }}
            division-filter(v-if="showDivisionFilter" v-model="selectedDivisions" :period="period")
            status-filter(v-model="selectedStatuses" :period="period" @statuses-loaded="statusesLoaded")
            documents-table(
              :period="period"
              :documents="documents"
              :loading="loading"
              :update-documents="updateDocuments"
              @change-document-comment="changeDocumentComment"
              @add-status="refetchDocuments"
            )
      v-tab-item
        v-list
          v-list-item(v-for="organization in organizationsHasNotDocument" :key="organization.id")
            v-list-item-content {{ organization.name }}
left-navigator-container(v-else :bread-crumbs="breadCrumbs" @update-drawer="$emit('update-drawer')")
  template(#header) {{ $t('dcis.documents.name') }}
    template(v-if="period.canAddAnyDivisionDocument || userPeriodDivision.length")
      v-spacer
      add-document-menu(
        v-slot="{ on, attrs }"
        :period="period"
        :documents="documents"
        :add-document-update="addDocumentUpdate"
        :add-document-data-update="addDocumentDataUpdate"
        :user-divisions="userPeriodDivision"
      )
        v-btn(v-on="on" v-bind="attrs" color="primary") {{ $t('dcis.documents.addDocument.buttonText') }}
  template(#subheader) {{ $t('shownOf', { count, totalCount }) }}
  division-filter(v-if="showDivisionFilter" v-model="selectedDivisions" :period="period")
  status-filter(v-model="selectedStatuses" :period="period" @statuses-loaded="statusesLoaded")
  documents-table(
    :period="period"
    :documents="documents"
    :loading="loading"
    :update-documents="updateDocuments"
    @change-document-comment="changeDocumentComment"
    @add-status="refetchDocuments"
  )
</template>

<script lang="ts">
import { useMutation } from '@vue/apollo-composable'
import { DataProxy } from 'apollo-cache'
import type { PropType } from '#app'
import { computed, defineComponent, ref, useNuxt2Meta, useRoute } from '#app'
import { useAuthStore } from '~/stores'
import { useFilters, useCursorPagination, useCommonQuery } from '~/composables'
import { useDocumentsQuery } from '~/services/grapqhl/queries/dcis/documents'
import { BreadCrumbsItem } from '~/types/devind'
import {
  ChangeDocumentCommentMutation,
  ChangeDocumentCommentMutationVariables,
  DivisionModelType,
  DocumentType,
  PeriodType,
  StatusType,
  OrganizationsHasNotDocumentQuery,
  OrganizationsHasNotDocumentQueryVariables
} from '~/types/graphql'
import { AddDocumentsDataMutationsResultType } from '~/components/dcis/documents/AddDocumentData.vue'
import { AddDocumentMutationResultType } from '~/components/dcis/documents/AddDocument.vue'
import statusesQuery from '~/gql/dcis/queries/statuses.graphql'
import organizationsHasNotDocumentQuery from '~/gql/dcis/queries/organizations_has_not_document.graphql'
import changeDocumentCommentMutation from '~/gql/dcis/mutations/document/change_document_comment.graphql'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import AddDocumentMenu from '~/components/dcis/documents/AddDocumentMenu.vue'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import DivisionFilter from '~/components/dcis/documents/DivisionFilter.vue'
import StatusFilter from '~/components/dcis/documents/StatusFilter.vue'
import DocumentsTable from '~/components/dcis/documents/DocumentsTable.vue'

export default defineComponent({
  components: {
    BreadCrumbs,
    AddDocumentMenu,
    LeftNavigatorContainer,
    DivisionFilter,
    StatusFilter,
    DocumentsTable
  },
  middleware: 'auth',
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true }
  },
  setup (props) {
    const route = useRoute()
    const { dateTimeHM } = useFilters()
    useNuxt2Meta({ title: props.period.name })
    const userStore = useAuthStore()

    const userPeriodDivision = computed(() => {
      const userDivisionIds = userStore.user.divisions.map((division: DivisionModelType) => division.id)
      return props.period.divisions.filter((division: DivisionModelType) => userDivisionIds.includes(division.id))
    })

    const selectedDivisions = ref<DivisionModelType[]>([])
    const selectedStatuses = ref<StatusType[]>([])

    const documentsQueryEnabled = ref<boolean>(false)
    const {
      data: documents,
      loading,
      pagination: { count, totalCount },
      update: updateDocuments,
      addUpdate,
      changeUpdate,
      refetch: refetchDocuments
    } = useDocumentsQuery(
      route.params.periodId,
      computed(() => selectedDivisions.value.map(division => division.id)),
      computed(() => selectedStatuses.value.map(status => status.id)),
      documentsQueryEnabled, {
        pagination: useCursorPagination(),
        fetchScroll: typeof document === 'undefined' ? null : document
      }
    )

    const statusesLoaded = () => {
      if (!documentsQueryEnabled.value) {
        documentsQueryEnabled.value = true
      }
    }

    const addDocumentUpdate = (cache: DataProxy, result: AddDocumentMutationResultType) => {
      if (!result.data.addDocument.errors.length) {
        addUpdate(cache, result, 'document')
      }
    }

    const addDocumentDataUpdate = (cache: DataProxy, result: AddDocumentsDataMutationsResultType) => {
      if (!result.data.addDocumentData.errors.length) {
        addUpdate(cache, result, 'documents')
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

    const showDivisionFilter = computed<boolean>(() => props.period.multiple)

    const { data: organizationsHasNotDocument } = useCommonQuery<
      OrganizationsHasNotDocumentQuery,
      OrganizationsHasNotDocumentQueryVariables
    >({
      document: organizationsHasNotDocumentQuery,
      variables: () => ({
        periodId: props.period.id
      })
    })

    return {
      statusesQuery,
      userPeriodDivision,
      selectedDivisions,
      selectedStatuses,
      documents,
      loading,
      count,
      totalCount,
      updateDocuments,
      refetchDocuments,
      statusesLoaded,
      addDocumentUpdate,
      addDocumentDataUpdate,
      dateTimeHM,
      changeDocumentComment,
      showDivisionFilter,
      organizationsHasNotDocument
    }
  }
})
</script>
