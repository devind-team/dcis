<template lang="pug">
  left-navigator-container(:bread-crumbs="bc"  @update-drawer="$emit('update-drawer')")
    template(#header) Настройка объектов сбора
    divisions(
      :period="period",
      :divisions="period.project.contentType.model === 'department' ? departments : organizations"
      :loading="organizationsLoading"
    )
</template>

<script lang="ts">
import type { ComputedRef, PropType } from '#app'
import { computed, defineComponent } from '#app'
import {
  DepartmentsQuery,
  DepartmentsQueryVariables,
  OrganizationsQuery,
  OrganizationsQueryVariables,
  OrganizationType,
  PeriodType
} from '~/types/graphql'
import { BreadCrumbsItem } from '~/types/devind'
import { useCommonQuery, useQueryRelay, useCursorPagination, useI18n } from '~/composables'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import Divisions from '~/components/dcis/periods/Divisions.vue'
import departmentQuery from '~/gql/dcis/queries/departments.graphql'
import organizationsQuery from '~/gql/dcis/queries/organizations.graphql'

export default defineComponent({
  components: { LeftNavigatorContainer, Divisions },
  middleware: 'auth',
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true }
  },
  setup (props) {
    const { localePath } = useI18n()

    const {
      data: departments,
      loading: departmentsLoading
    } = useCommonQuery<DepartmentsQuery, DepartmentsQueryVariables>({
      document: departmentQuery
    })
    const {
      data: organizations,
      loading: organizationsLoading
    } = useQueryRelay<OrganizationsQuery, OrganizationsQueryVariables, OrganizationType>({
      document: organizationsQuery,
      options: { fetchPolicy: 'network-only' }
    }, {
      pagination: useCursorPagination(),
      fetchScroll: typeof document === 'undefined' ? null : document
    })

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      { text: 'Настройка объектов сбора', to: localePath({ name: 'dcis-periods-periodId-divisions' }), exact: true }
    ]))

    return { bc, departments, organizations, departmentsLoading, organizationsLoading }
  }
})
</script>
