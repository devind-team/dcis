<template lang="pug">
bread-crumbs(:items="bc")
  apollo-mutation(
    v-slot="{ mutate, loading, error }"
    :mutation="require('~/gql/dcis/mutations/period/change_period.graphql')"
    :variables="{ id: period.id, name, status, start, expiration, multiple, privately, versioning }"
    :update="changePeriodUpdate"
    tag
  )
    v-card
      template(v-if="period.canChangeSettings")
        v-card-title
          v-app-bar-nav-icon(v-if="$vuetify.breakpoint.smAndDown" @click="$emit('update-drawer')")
          | {{ $t('dcis.periods.changePeriod.header') }}
        v-card-subtitle {{ period.name }}
        validation-observer(v-slot="{ handleSubmit, invalid }")
          form(@submit.prevent="handleSubmit(mutate)")
            v-card-text
              v-alert(type="success" :value="successUpdate") {{ $t('mutationSuccess')}}
              v-alert(
                type="error"
                :value="!!error"
                dismissible
              ) {{ $t('mutationBusinessLogicError', { error: error }) }}
              validation-provider(
                v-slot="{ errors, valid }"
                :name="String($t('dcis.periods.changePeriod.name'))"
                rules="required|min:3|max:250"
              )
                v-text-field(
                  v-model="name"
                  :label="$t('dcis.periods.changePeriod.name')"
                  :error-messages="errors" :success="valid"
                  counter
                )
              v-autocomplete(
                v-model="status"
                :items="statusItems"
                :label="$t('dcis.periods.changePeriod.status')"
                item-text="name"
                item-value="value"
                success
              )
              v-menu(
                v-model="chooseStart"
                :close-on-content-click="false"
                bottom max-width="290px"
                transition="scale-transition"
                min-width="290px"
              )
                template(#activator="{ on }")
                  v-text-field(
                    v-on="on"
                    v-model="start"
                    :label="$t('dcis.periods.changePeriod.start')"
                    success
                    readonly
                  )
                v-date-picker(v-model="start" @input="chooseStart = false")
              v-menu(
                v-model="chooseExpiration"
                :close-on-content-click="false"
                bottom max-width="290px"
                transition="scale-transition"
                min-width="290px"
              )
                template(#activator="{ on }")
                  v-text-field(
                    v-on="on"
                    v-model="expiration"
                    :label="$t('dcis.periods.changePeriod.expiration')"
                    success
                    readonly
                  )
                v-date-picker(v-model="expiration" @input="chooseExpiration = false")
              v-row
                v-col(cols="12" md="6")
                  v-checkbox(v-model="multiple" :label="$t('dcis.periods.changePeriod.multiple')")
                v-col(cols="12" md="6")
                  v-checkbox(v-model="privately" :label="$t('dcis.periods.changePeriod.privately')")
                v-col(cols="12" md="6")
                  v-checkbox(v-model="versioning" :label="$t('dcis.periods.changePeriod.versioning')")
            v-card-actions
              v-btn(
                :disabled="invalid"
                :loading="loading"
                type="submit"
                color="success"
              ) {{$t('dcis.periods.changePeriod.save')}}
      v-divider(v-if="period.canChangeSettings && period.canDelete")
      template(v-if="period.canDelete")
        v-card-title {{ $t('dcis.periods.deletePeriod.header') }}
        v-card-text
          v-alert(type="warning") {{ $t('dcis.periods.deletePeriod.warning') }}
        v-card-actions
          apollo-mutation(
            v-slot="{ mutate }"
            :mutation="require('~/gql/dcis/mutations/period/delete_period.graphql')"
            :variables="{ id: period.id}"
            @done="deletePeriodDone"
            tag
          )
            delete-menu(
              v-slot="{ on }"
              :itemName="String($t('dcis.periods.deletePeriod.itemName'))"
              @confirm="mutate"
            )
              v-btn(v-on="on" color="error") {{ $t('dcis.periods.deletePeriod.delete') }}
</template>

<script lang="ts">
import { promiseTimeout } from '@vueuse/core'
import { DataProxy } from 'apollo-cache'
import type { PropType } from '#app'
import { computed, defineComponent, ref, useNuxt2Meta, useRouter, inject } from '#app'
import { BreadCrumbsItem } from '~/types/devind'
import {
  PeriodType,
  ChangePeriodMutationPayload,
  DeletePeriodMutationPayload
} from '~/types/graphql'
import { useI18n } from '~/composables'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import DeleteMenu from '~/components/common/menu/DeleteMenu.vue'

type ChangePeriodResultMutation = { data: { changePeriod: ChangePeriodMutationPayload } }
type DeletePeriodResultMutation = { data: { deletePeriod: DeletePeriodMutationPayload } }
type ChangePeriodUpdateType = (cache: DataProxy, result: ChangePeriodResultMutation) => DataProxy

type StatusItems = {
  name: string
  value: string
}

export default defineComponent({
  components: { BreadCrumbs, DeleteMenu },
  middleware: 'auth',
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true }
  },
  setup (props) {
    useNuxt2Meta({ title: props.period.name })

    const { t, localePath } = useI18n()

    const router = useRouter()

    if (!(props.period.canChangeSettings || props.period.canDelete)) {
      router.push(localePath({ name: 'dcis-periods-periodId-documents' }))
    }

    const periodChangeUpdate = inject<ChangePeriodUpdateType>('periodChangeUpdate')

    const name = ref<string>(props.period.name)
    const multiple = ref<boolean>(props.period.multiple)
    const privately = ref<boolean>(props.period.privately)
    const versioning = ref<boolean>(props.period.versioning)
    const start = ref<string>(props.period.start)
    const expiration = ref<string>(props.period.expiration)

    const chooseStart = ref<boolean>(false)
    const chooseExpiration = ref<boolean>(false)

    const successUpdate = ref<boolean>(false)
    const statusItems: StatusItems[] = [
      { name: t('dcis.periods.statuses.preparation') as string, value: 'preparation' },
      { name: t('dcis.periods.statuses.open') as string, value: 'open' },
      { name: t('dcis.periods.statuses.close') as string, value: 'close' }
    ]
    const status = ref<string>(props.period.status)

    const bc = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      {
        text: t('dcis.periods.links.settings') as string,
        to: localePath({ name: 'dcis-periods-periodId-settings' }),
        exact: true
      }
    ]))

    const changePeriodUpdate = (cache: DataProxy, result: ChangePeriodResultMutation) => {
      const { success } = result.data.changePeriod
      if (success) {
        periodChangeUpdate(cache, result)
        successUpdate.value = true
        promiseTimeout(5000).then(() => (successUpdate.value = false))
      }
    }

    const deletePeriodDone = ({ data: { deletePeriod: { success, deleteId } } }: DeletePeriodResultMutation) => {
      if (success) {
        router.push(localePath({
          name: 'dcis-projects-projectId-periods',
          params: { projectId: props.period.project.id },
          query: { deletePeriodId: deleteId }
        }))
      }
    }

    return {
      bc,
      name,
      multiple,
      privately,
      versioning,
      start,
      expiration,
      status,
      statusItems,
      chooseStart,
      chooseExpiration,
      successUpdate,
      changePeriodUpdate,
      deletePeriodDone
    }
  }
})
</script>
