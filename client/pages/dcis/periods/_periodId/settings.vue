<template lang="pug">
  bread-crumbs(:items="bc")
    apollo-mutation(
      v-slot="{ mutate, loading, error }"
      :mutation="require('~/gql/dcis/mutations/project/change_period.graphql')"
      :variables="{ id: period.id, name, status, start, expiration, multiple, privately }"
      :update="changePeriodUpdate"
      tag
    )
      v-card
        v-card-title
          v-app-bar-nav-icon(v-if="$vuetify.breakpoint.smAndDown" @click="$emit('update-drawer')")
          | {{ $t('dcis.periods.header') }}
        v-card-subtitle {{ period.name }}
        validation-observer(v-slot="{ handleSubmit, invalid }")
          form(@submit.prevent="handleSubmit(mutate)")
            v-card-text
              v-alert(type="success" :value="successUpdate") {{ $t('mutationSuccess')}}
              v-alert(type="error" :value="!!error" dismissible) {{ $t('mutationBusinessLogicError', { error: error }) }}
              validation-provider(
                v-slot="{ errors, valid }"
                :name="String($t('dcis.periods.name'))"
                rules="required|min:3|max:250"
              )
                v-text-field(
                  v-model="name"
                  :label="$t('dcis.periods.name')"
                  :error-messages="errors" :success="valid"
                  counter
                )
              v-autocomplete(v-model="status" :items="items" label="Статус" item-text="name" item-value="value" success)
              v-menu(
                v-model="chooseStart"
                :close-on-content-click="false"
                bottom max-width="290px"
                transition="scale-transition"
                min-width="290px"
              )
                template(v-slot:activator="{ on }")
                  v-text-field(
                    v-on="on"
                    v-model="start"
                    :label="$t('dcis.periods.start')"
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
                template(v-slot:activator="{ on }")
                  v-text-field(
                    v-on="on"
                    v-model="expiration"
                    :label="$t('dcis.periods.expiration')"
                    success
                    readonly
                  )
                v-date-picker(v-model="expiration" @input="chooseExpiration = false")
              v-row
                v-col(cols="12" md="6")
                  v-checkbox(v-model="multiple" :label="$t('dcis.periods.multiple')")
                v-col(cols="12" md="6")
                  v-checkbox(v-model="privately" :label="$t('dcis.periods.privately')")
            v-card-actions
              v-btn(
                v-if="period.user && period.user.id === user.id || hasPerm('dcis.change_period')"
                :disabled="invalid"
                :loading="loading"
                type="submit"
                color="success"
              ) {{$t('dcis.periods.actions.save')}}
        v-divider
        v-card-title {{ $t('dcis.periods.delete') }}
        v-card-text
          v-alert(type="warning") {{ $t('dcis.periods.deleteWarning') }}
        v-card-actions
          apollo-mutation(
            v-slot="{ mutate }"
            :mutation="require('~/gql/dcis/mutations/project/delete_period.graphql')"
            :variables="{ id: period.id}"
            @done="deletePeriodDone"
            tag
          )
            delete-menu(
              v-if="period.user && period.user.id === user.id || hasPerm('dcis.delete_period')"
              v-slot="{ on }"
              :itemName="String($t('dcis.periods.deleteItemName'))"
              @confirm="mutate"
            )
              v-btn(v-on="on" color="error") {{ $t('dcis.periods.actions.delete') }}
</template>

<script lang="ts">
import { promiseTimeout } from '@vueuse/core'
import { DataProxy } from 'apollo-cache'
import type { Ref, ComputedRef, PropType } from '#app'
import { computed, defineComponent, ref, toRefs, useNuxt2Meta, useRouter, inject } from '#app'
import { BreadCrumbsItem } from '~/types/devind'
import {
  ChangePeriodMutationPayload,
  DeletePeriodMutationPayload,
  PeriodType,
  UserType
} from '~/types/graphql'
import { HasPermissionFnType, useAuthStore } from '~/store'
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
    const authStore = useAuthStore()
    const { localePath } = useI18n()
    const router = useRouter()
    const { user, hasPerm } = toRefs<{ user: UserType, hasPerm: HasPermissionFnType }>(authStore)

    useNuxt2Meta({ title: props.period.name })

    const changeUpdate: ChangePeriodUpdateType = inject<ChangePeriodUpdateType>('changeUpdate')

    const name: Ref<string> = ref<string>(props.period.name)
    const multiple: Ref<boolean> = ref<boolean>(props.period.multiple)
    const privately: Ref<boolean> = ref<boolean>(props.period.privately)
    const start: Ref<string> = ref<string>(props.period.start)
    const expiration: Ref<string> = ref<string>(props.period.expiration)

    const chooseStart: Ref<boolean> = ref<boolean>(false)
    const chooseExpiration: Ref<boolean> = ref<boolean>(false)

    const successUpdate: Ref<boolean> = ref<boolean>(false)
    const items: StatusItems[] = [
      { name: 'Подготовка', value: 'preparation' },
      { name: 'Заполнение', value: 'open' },
      { name: 'Сбор закрыт', value: 'close' }
    ]
    const status: Ref<string> = ref<string>(props.period.status)

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      { text: 'Настройки', to: localePath({ name: 'dcis-periods-periodId-settings' }), exact: true }
    ]))

    const changePeriodUpdate = (cache: DataProxy, result: ChangePeriodResultMutation) => {
      const { success } = result.data.changePeriod
      if (success) {
        changeUpdate(cache, result)
        successUpdate.value = true
        promiseTimeout(5000).then(() => (successUpdate.value = false))
      }
    }

    const deletePeriodDone = ({ data: { deletePeriod: { success, deletedId } } }: DeletePeriodResultMutation) => {
      if (success) {
        router.push(localePath({
          name: 'dcis-projects-projectId-periods',
          params: { projectId: props.period.project.id },
          query: { periodId: deletedId }
        }))
      }
    }

    return {
      bc,
      name,
      multiple,
      privately,
      start,
      expiration,
      status,
      user,
      items,
      chooseStart,
      chooseExpiration,
      successUpdate,
      hasPerm,
      changePeriodUpdate,
      deletePeriodDone
    }
  }
})
</script>
