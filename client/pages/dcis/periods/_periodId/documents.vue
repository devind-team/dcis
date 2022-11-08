<template lang="pug">
left-navigator-container(:bread-crumbs="breadCrumbs" @update-drawer="$emit('update-drawer')")
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
  items-data-filter(
    v-if="showDivisionFilter"
    v-model="selectedDivisions"
    v-bind="divisionFilterMessages"
    :items="period.divisions.map(d => ({ id: d.id, name: d.name }))"
    :get-name="d => d.name"
    :search-function="(d, s) => d.name.toLocaleLowerCase().includes(s.toLocaleLowerCase())"
    message-container-class="mr-1 mb-1"
    multiple
    has-select-all
  )
  items-data-filter(
    ref="statusesFilter"
    v-model="selectedStatuses"
    v-bind="statusFilterMessages"
    :items="statuses ? statuses : []"
    :get-name="status => status.name"
    message-container-class="mr-1 mb-1"
    multiple
    has-select-all
  )
  v-data-table(
    :headers="headers"
    :items="documents"
    :loading="loading"
    disable-sort
    disable-pagination
    hide-default-footer
  )
    template(#item.division="{ item }")
      nuxt-link(
        :to="localePath({ name: 'dcis-documents-documentId', params: { documentId: item.id } })"
      ) {{ item.objectName }} ({{ item.objectId }})
    template(#item.version="{ item }")
      template(v-if="period.multiple") {{ item.version }}
      nuxt-link(
        v-else
        :to="localePath({ name: 'dcis-documents-documentId', params: { documentId: item.id } })"
      ) {{ item.version }}
    template(#item.comment="{ item }")
      template(v-if="item.comment")
        template(v-if="canChangeDocumentComment(item)")
          text-menu(v-slot="{ on }" @update="changeDocumentComment(item, $event)" :value="item.comment")
            a(v-on="on") {{ item.comment }}
        template(v-else) {{ item.comment }}
    template(#item.lastStatus="{ item }")
      template(v-if="item.lastStatus")
        document-statuses(
          :can-delete="canDeleteDocumentStatus(item)"
          :update="updateDocuments"
          :document="item"
          @add-status="refetchDocuments"
        )
          template(#activator="{ on }")
            a(v-on="on" class="font-weight-bold") {{ item.lastStatus.status.name }}.
        div {{ $t('dcis.documents.tableItems.statusAssigned', { assigned: dateTimeHM(item.lastStatus.createdAt) }) }}
        .font-italic {{ item.lastStatus.comment }}
    template(v-for="dti in ['createdAt', 'updatedAt']" v-slot:[`item.${dti}`]="{ item }") {{ dateTimeHM(item[dti]) }}
</template>

<script lang="ts">
import { useMutation } from '@vue/apollo-composable'
import { DataProxy } from 'apollo-cache'
import { DataTableHeader } from 'vuetify'
import type { PropType } from '#app'
import { computed, defineComponent, ref, useNuxt2Meta, useRoute, onMounted, watch, nextTick } from '#app'
import { useAuthStore } from '~/stores'
import { useFilters, useI18n, useCursorPagination, useCommonQuery } from '~/composables'
import { useDocumentsQuery } from '~/services/grapqhl/queries/dcis/documents'
import { BreadCrumbsItem } from '~/types/devind'
import {
  ChangeDocumentCommentMutation,
  ChangeDocumentCommentMutationVariables,
  DivisionModelType,
  DocumentType,
  PeriodType,
  StatusType,
  StatusFieldsFragment,
  StatusesQuery,
  StatusesQueryVariables
} from '~/types/graphql'
import { FilterMessages } from '~/types/filters'
import changeDocumentCommentMutation from '~/gql/dcis/mutations/document/change_document_comment.graphql'
import { AddDocumentsDataMutationsResultType } from '~/components/dcis/documents/AddDocumentData.vue'
import { AddDocumentMutationResultType } from '~/components/dcis/documents/AddDocument.vue'
import AddDocumentMenu from '~/components/dcis/documents/AddDocumentMenu.vue'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import ItemsDataFilter from '~/components/common/filters/ItemsDataFilter.vue'
import DocumentStatuses from '~/components/dcis/documents/DocumentStatuses.vue'
import TextMenu from '~/components/common/menu/TextMenu.vue'
import statusesQuery from '~/gql/dcis/queries/statuses.graphql'

export default defineComponent({
  components: {
    AddDocumentMenu,
    LeftNavigatorContainer,
    ItemsDataFilter,
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

    const statusesFilter = ref<InstanceType<typeof ItemsDataFilter> | null>(null)

    onMounted(() => {
      watch(() => statuses.value, (statuses: StatusFieldsFragment[]) => {
        if (props.period.isCurator && statuses) {
          const inputCompleted = statuses.find((status: StatusType) => status.name === 'Ввод завершен')
          if (inputCompleted) {
            nextTick(() => {
              statusesFilter.value.select([inputCompleted])
            })
          }
        }
        if (!documentsQueryEnabled.value) {
          documentsQueryEnabled.value = true
        }
      }, { immediate: true })
    })

    const userPeriodDivision = computed(() => {
      const userDivisionIds = userStore.user.divisions.map((division: DivisionModelType) => division.id)
      return props.period.divisions.filter((division: DivisionModelType) => userDivisionIds.includes(division.id))
    })

    const canChangeDocumentComment = (document: DocumentType) => {
      return document.canChange || document.user?.id === userStore.user.id
    }
    const canDeleteDocumentStatus = (document: DocumentType) => {
      return document.canChange
    }

    const { data: statuses } = useCommonQuery<
      StatusesQuery,
      StatusesQueryVariables
    >({
      document: statusesQuery
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

    const divisionFilterMessages = computed<FilterMessages>(() => {
      const filterName = props.period.project.contentType.model === 'department'
        ? 'divisionFilterDepartment'
        : 'divisionFilterOrganization'
      return getFilterMessages(filterName, true)
    })
    const statusFilterMessages = computed<FilterMessages>(() => {
      return getFilterMessages('statusFilter', true)
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

    const showDivisionFilter = computed<boolean>(() => props.period.multiple)
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

    return {
      statusesQuery,
      statusesFilter,
      userPeriodDivision,
      canChangeDocumentComment,
      canDeleteDocumentStatus,
      statuses,
      selectedDivisions,
      selectedStatuses,
      documents,
      loading,
      count,
      totalCount,
      updateDocuments,
      refetchDocuments,
      addDocumentUpdate,
      addDocumentDataUpdate,
      dateTimeHM,
      changeDocumentComment,
      divisionFilterMessages,
      statusFilterMessages,
      getFilterMessages,
      showDivisionFilter,
      headers
    }
  }
})
</script>
