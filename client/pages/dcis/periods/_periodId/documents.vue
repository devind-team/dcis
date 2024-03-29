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
            template(v-if="showDivisionFilter")
              organization-filter(
                v-if="period.project.contentType.model === 'organization'"
                v-model="selectedDivisions"
                :period="period"
                :title="String($t('dcis.periods.organizationFilter.title'))"
                message-container-class="mb-2 mr-1"
              )
              department-filter(
                v-else
                v-model="selectedDivisions"
                :period="period"
                :title="String($t('dcis.periods.departmentFilter.title'))"
                message-container-class="mb-2 mr-1"
              )
            document-status-filter(
              v-model="selectedStatuses"
              :period="period"
              message-container-class="mb-2 mr-1"
              @statuses-loaded="statusesLoaded"
            )
            documents-table(
              :period="period"
              :documents="documents"
              :loading="loading"
              :update-documents="updateDocuments"
              @add-status="refetchDocuments"
              @update-order-by="orderBy = $event"
            )
      v-tab-item
        v-list
          v-list-item(v-for="organization in organizationsWithoutDocument" :key="organization.id")
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
  template(v-if="showDivisionFilter")
    organization-filter(
      v-if="period.project.contentType.model === 'organization'"
      v-model="selectedDivisions"
      :period="period"
      :title="String($t('dcis.periods.organizationFilter.title'))"
      message-container-class="mb-2 mr-1"
    )
    department-filter(
      v-else
      v-model="selectedDivisions"
      :period="period"
      :title="String($t('dcis.periods.departmentFilter.title'))"
      message-container-class="mb-2 mr-1"
    )
  document-status-filter(
    v-model="selectedStatuses"
    :period="period"
    message-container-class="mr-1 mb-1"
    @statuses-loaded="statusesLoaded"
  )
  documents-table(
    :period="period"
    :documents="documents"
    :loading="loading"
    :update-documents="updateDocuments"
    @change-document-comment="changeDocumentComment"
    @add-status="refetchDocuments"
    @update-order-by="orderBy = $event"
  )
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import type { PropType } from '#app'
import { computed, defineComponent, ref, useNuxt2Meta, useRoute } from '#app'
import { useAuthStore } from '~/stores'
import { useFilters, useCursorPagination, useCommonQuery, useQueryRelay } from '~/composables'
import { BreadCrumbsItem } from '~/types/devind'
import {
  DivisionModelType,
  DocumentType,
  PeriodType,
  StatusType,
  OrganizationsWithoutDocumentQuery,
  OrganizationsWithoutDocumentQueryVariables, DocumentsQuery, DocumentsQueryVariables
} from '~/types/graphql'
import { AddDocumentsDataMutationsResultType } from '~/components/dcis/documents/AddDocumentData.vue'
import { AddDocumentMutationResultType } from '~/components/dcis/documents/AddDocument.vue'
import statusesQuery from '~/gql/dcis/queries/statuses.graphql'
import organizationsWithoutDocumentQuery from '~/gql/dcis/queries/organizations_without_document.graphql'
import documentsQuery from '~/gql/dcis/queries/documents.graphql'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import AddDocumentMenu from '~/components/dcis/documents/AddDocumentMenu.vue'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import DocumentStatusFilter from '~/components/dcis/periods/DocumentStatusFilter.vue'
import DocumentsTable from '~/components/dcis/documents/DocumentsTable.vue'
import OrganizationFilter from '~/components/dcis/periods/OrganizationFilter.vue'
import DepartmentFilter from '~/components/dcis/periods/DepartmentFilter.vue'

export default defineComponent({
  components: {
    BreadCrumbs,
    AddDocumentMenu,
    LeftNavigatorContainer,
    DocumentStatusFilter,
    DocumentsTable,
    OrganizationFilter,
    DepartmentFilter
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

    const orderBy = ref<string[]>([])

    const documentsQueryEnabled = ref<boolean>(false)
    const {
      data: documents,
      loading,
      pagination: { count, totalCount },
      update: updateDocuments,
      addUpdate,
      refetch: refetchDocuments
    } = useQueryRelay<DocumentsQuery, DocumentsQueryVariables, DocumentType>({
      document: documentsQuery,
      variables: () => ({
        periodId: route.params.periodId,
        divisionIds: selectedDivisions.value.map(division => division.id),
        lastStatusIds: selectedStatuses.value.map(status => status.id),
        orderBy: orderBy.value
      }),
      options: computed(() => ({
        enabled: documentsQueryEnabled.value
      }))
    },
    {
      pagination: useCursorPagination(),
      fetchScroll: typeof document === 'undefined' ? null : document
    })

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

    const showDivisionFilter = computed<boolean>(() => props.period.multiple)

    const { data: organizationsWithoutDocument } = useCommonQuery<
      OrganizationsWithoutDocumentQuery,
      OrganizationsWithoutDocumentQueryVariables
    >({
      document: organizationsWithoutDocumentQuery,
      variables: () => ({
        periodId: props.period.id
      }),
      options: computed(() => ({
        enabled: props.period.isAdmin || props.period.isCurator
      }))
    })

    return {
      statusesQuery,
      userPeriodDivision,
      selectedDivisions,
      selectedStatuses,
      orderBy,
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
      showDivisionFilter,
      organizationsWithoutDocument
    }
  }
})
</script>
