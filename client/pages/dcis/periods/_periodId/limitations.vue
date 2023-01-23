<template lang="pug">
left-navigator-container(:bread-crumbs="bc" @update-drawer="$emit('update-drawer')")
  template(#header) {{ $t('dcis.periods.limitations.name') }}
    template(v-if="period.canChangeLimitations")
      v-spacer
      change-period-limitations-menu(
        :period="period"
        :from-file-update="limitationsResetUpdate"
        :add-update="limitationsAddUpdate"
      )
        template(#activator="{ on, attrs }")
          v-btn(v-on="on" v-bind="attrs" color="primary") {{ $t('dcis.periods.limitations.changeMenu.buttonText') }}
  template(#subheader) {{ $t('shownOf', { count, totalCount: count }) }}
  v-data-table(
    :headers="tableHeaders"
    :items="limitations"
    :loading="limitationsLoading"
    disable-pagination
    hide-default-footer
  )
    template(#item.actions="{ item }")
      change-period-limitation(:period="period" :limitation="item")
        template(#activator="{ on: onMenu, attrs: attrsMenu }")
          v-tooltip(bottom)
            template(#activator="{ on: onTooltip, attrs: attrsTooltip }")
              v-btn.mr-1(
                v-on="{ ...onMenu, ...onTooltip }"
                v-bind="{ ...attrsMenu, ...attrsTooltip}"
                color="primary"
                icon
              )
                v-icon mdi-pencil
            span {{ String($t('dcis.periods.limitations.tooltips.change')) }}
      delete-menu(
        :item-name="String($t('dcis.periods.limitations.deleteItemName'))"
        @confirm="deleteLimitation({ limitationId: item.id })"
      )
        template(#default="{ on: onMenu }")
          v-tooltip(bottom)
            template(#activator="{ on: onTooltip, attrs }")
              v-btn.ml-1(v-on="{ ...onMenu, ...onTooltip }" v-bind="attrs" icon, color="error")
                v-icon mdi-delete
            span {{ String($t('dcis.periods.limitations.tooltips.delete')) }}
</template>

<script lang="ts">
import { computed, defineComponent, useNuxt2Meta } from '#app'
import type { PropType } from '#app'
import { DataTableHeader } from 'vuetify'
import { useMutation } from '@vue/apollo-composable'
import { BreadCrumbsItem } from '~/types/devind'
import {
  PeriodType,
  LimitationsQuery,
  LimitationsQueryVariables,
  DeleteLimitationMutation,
  DeleteLimitationMutationVariables
} from '~/types/graphql'
import { useI18n, useCommonQuery } from '~/composables'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import ChangePeriodLimitationsMenu from '~/components/dcis/periods/ChangePeriodLimitationsMenu.vue'
import ChangePeriodLimitation from '~/components/dcis/periods/ChangePeriodLimitation.vue'
import DeleteMenu from '~/components/common/menu/DeleteMenu.vue'
import limitationsQuery from '~/gql/dcis/queries/limitations.graphql'
import deleteLimitationMutation from '~/gql/dcis/mutations/limitation/delete_limitation.graphql'

export default defineComponent({
  components: { LeftNavigatorContainer, ChangePeriodLimitationsMenu, ChangePeriodLimitation, DeleteMenu },
  middleware: 'auth',
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true }
  },
  setup (props) {
    const { t, localePath } = useI18n()
    useNuxt2Meta({ title: props.period.name })

    const bc = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      {
        text: t('dcis.periods.limitations.name') as string,
        to: localePath({ name: 'dcis-periods-periodId-limitations' }),
        exact: true
      }
    ]))

    const tableHeaders = computed<DataTableHeader[]>(() => {
      const result: DataTableHeader[] = [
        { text: t('dcis.periods.limitations.tableHeaders.sheet') as string, value: 'sheet.name' },
        { text: t('dcis.periods.limitations.tableHeaders.formula') as string, value: 'formula' },
        { text: t('dcis.periods.limitations.tableHeaders.errorMessage') as string, value: 'errorMessage' }
      ]
      if (props.period.canChangeLimitations) {
        result.push({
          text: t('dcis.periods.limitations.tableHeaders.actions') as string,
          value: 'actions',
          align: 'center',
          sortable: false
        })
      }
      return result
    })

    const {
      data: limitations,
      loading: limitationsLoading,
      resetUpdate: limitationsResetUpdate,
      addUpdate: limitationsAddUpdate,
      deleteUpdate: limitationDeleteUpdate
    } = useCommonQuery<
      LimitationsQuery,
      LimitationsQueryVariables
    >({
      document: limitationsQuery,
      variables: () => ({
        periodId: props.period.id
      })
    })
    const count = computed<number>(() => limitations.value ? limitations.value.length : 0)

    const { mutate: deleteLimitation } = useMutation<
      DeleteLimitationMutation,
      DeleteLimitationMutationVariables
    >(deleteLimitationMutation, {
      update: limitationDeleteUpdate
    })

    return {
      bc,
      tableHeaders,
      limitations,
      limitationsLoading,
      limitationsResetUpdate,
      limitationsAddUpdate,
      count,
      deleteLimitation
    }
  }
})
</script>
