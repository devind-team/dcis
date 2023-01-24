<template lang="pug">
bread-crumbs(:items="bc")
  apollo-mutation(
    v-slot="{ mutate, loading, error }"
    :mutation="require('~/gql/dcis/mutations/period/unload_period.graphql')"
    :variables="variables"
    @done="unloadPeriodOnDone"
    @error="unloadPeriodOnError"
    tag
  )
    v-card
      v-card-title.pb-0
        v-app-bar-nav-icon(v-if="$vuetify.breakpoint.smAndDown" @click="$emit('update-drawer')")
        | {{ $t('dcis.periods.unload.name') }}
      form(@submit.prevent="mutate")
        v-card-text
          mutation-result-alert(ref="mutationResultAlert")
          organization-filter(
            v-model="selectedOrganizations"
            :period="period"
            :title="String($t('dcis.periods.unload.organizationsFilterTitle'))"
            message-container-class="mr-1"
          )
          status-filter(
            v-model="selectedStatuses"
            :period="period"
            :title="String($t('dcis.periods.unload.statusFilterTitle'))"
            message-container-class="mr-1"
          )
          v-checkbox(v-model="unloadWithoutDocument" :label="$t('dcis.periods.unload.unloadWithoutDocument')")
          v-checkbox(v-model="unloadDefault" :label="$t('dcis.periods.unload.unloadDefault')")
          v-checkbox(v-model="applyNumberFormat" :label="$t('dcis.periods.unload.applyNumberFormat')")
          v-select(v-model="sheets" :label="$t('dcis.periods.unload.sheets.label')" :items="sheetsItems")
          v-text-field(v-model="emptyCell" :label="$t('dcis.periods.unload.emptyCell')")
        v-card-actions
          v-btn(:loading="loading" type="submit" color="primary") {{ $t('upload') }}
</template>

<script lang="ts">
import { ref, computed, defineComponent, PropType } from '#app'
import { ApolloError } from 'apollo-client'
import { useI18n } from '~/composables'
import { BreadCrumbsItem } from '~/types/devind'
import {
  PeriodType,
  OrganizationType,
  StatusType,
  UnloadPeriodMutation,
  UnloadPeriodMutationVariables, ErrorFieldType
} from '~/types/graphql'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import MutationResultAlert from '~/components/common/MutationResultAlert.vue'
import OrganizationFilter from '~/components/dcis/periods/OrganizationFilter.vue'
import StatusFilter from '~/components/dcis/periods/StatusFilter.vue'

type UnloadPeriodMutationResult = { data: UnloadPeriodMutation }

export default defineComponent({
  components: { BreadCrumbs, MutationResultAlert, OrganizationFilter, StatusFilter },
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true }
  },
  setup (props) {
    const { t, localePath } = useI18n()

    const bc = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      {
        text: t('dcis.periods.unload.name') as string,
        to: localePath({ name: 'dcis-periods-periodId-unload' }),
        exact: true
      }
    ]))

    const mutationResultAlert = ref<InstanceType<typeof MutationResultAlert>>(null)

    const setApolloError = (error: ApolloError): void => {
      mutationResultAlert.value.setApolloError(error)
    }

    const setBusinessLogicError = (message: string): void => {
      mutationResultAlert.value.setError(message, 'BusinessLogicError')
    }

    const sheetsItems = computed<string[]>(() => [
      t('dcis.periods.unload.sheets.onlyHeads') as string,
      t('dcis.periods.unload.sheets.onlyChildren') as string,
      t('dcis.periods.unload.sheets.headsAndChildrens') as string
    ])

    const selectedOrganizations = ref<OrganizationType[]>([])
    const selectedStatuses = ref<StatusType[]>([])
    const unloadWithoutDocument = ref<boolean>(true)
    const unloadDefault = ref<boolean>(true)
    const applyNumberFormat = ref<boolean>(true)
    const unloadHeads = ref<boolean>(true)
    const unloadChildren = ref<boolean>(false)
    const emptyCell = ref<string>('')
    const sheets = computed<string>({
      get () {
        if (unloadHeads.value && !unloadChildren.value) {
          return sheetsItems.value[0]
        }
        if (!unloadHeads.value && unloadChildren.value) {
          return sheetsItems.value[1]
        }
        return sheetsItems.value[2]
      },
      set (value: string) {
        if (value === sheetsItems.value[0]) {
          unloadHeads.value = true
          unloadChildren.value = false
        }
        if (value === sheetsItems.value[1]) {
          unloadHeads.value = false
          unloadChildren.value = true
        }
        if (value === sheetsItems.value[2]) {
          unloadHeads.value = true
          unloadChildren.value = true
        }
      }
    })

    const variables = computed<UnloadPeriodMutationVariables>(() => ({
      periodId: props.period.id,
      organizationIds: selectedOrganizations.value.map((organization: OrganizationType) => organization.id),
      statusIds: selectedStatuses.value.map((status: StatusType) => status.id),
      unloadWithoutDocument: unloadWithoutDocument.value,
      unloadDefault: unloadDefault.value,
      applyNumberFormat: applyNumberFormat.value,
      unloadHeads: unloadHeads.value,
      unloadChildren: unloadChildren.value,
      emptyCell: emptyCell.value
    }))

    const unloadPeriodOnDone = ({ data: { unloadPeriod: { success, errors, src } } }: UnloadPeriodMutationResult) => {
      if (success) {
        window.open(src, '_blank')
      } else {
        const errorString = errors.reduce((a: string, c: ErrorFieldType) =>
          a ? `${a}, ${c.messages.join(', ')}` : c.messages.join(', '), '')
        setBusinessLogicError(errorString)
      }
    }

    const unloadPeriodOnError = (error: ApolloError): void => {
      setApolloError(error)
    }

    return {
      bc,
      mutationResultAlert,
      sheetsItems,
      selectedOrganizations,
      selectedStatuses,
      unloadPeriodOnDone,
      unloadWithoutDocument,
      unloadDefault,
      applyNumberFormat,
      sheets,
      emptyCell,
      variables,
      unloadPeriodOnError
    }
  }
})
</script>
