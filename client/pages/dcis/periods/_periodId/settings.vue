<template lang="pug">
  bread-crumbs(:items="bc")
    apollo-mutation(
      v-slot="{ mutate, loading, error }"
      @done="changePeriodDone"
      :mutation="require('~/gql/dcis/mutations/project/change_period.graphql')"
      :variables="{ id: period.id, name, status, start, multiple, expiration, privately }"
      tag
    )
      v-card
        v-row.align-center
          v-col(cols="12" md="3")
            v-card-title {{$t('dcis.periods.header')}}
            v-card-subtitle {{ period.name }}
          v-col(cols="12" md="8")
            v-alert(type="success" :value="successUpdate") {{ $t('mutationSuccess')}}
            v-alert(type="error" :value="!!error" dismissible) {{$t('mutationBusinessLogicError', { error: error})}}
        validation-observer(v-slot="{ handleSubmit, invalid }")
          form(@submit.prevent="handleSubmit(mutate)")
            v-card-text
              validation-provider(
                v-slot="{ errors, valid }"
                :name="$t('dcis.periods.name')"
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
                v-col(cols="12" md="2")
                  v-checkbox(v-model="multiple" :label="$t('dcis.periods.multiple')")
                v-col(cols="12" md="10")
                  v-checkbox(v-model="privately" :label="$t('dcis.periods.privately')")
            v-card-actions
              v-row
                v-col
                  apollo-mutation(
                    :mutation="require('~/gql/dcis/mutations/project/delete_period.graphql')"
                    :variables="{ id: period.id}"
                    @done="deletePeriodDone"
                  )
                    template(v-slot="{ mutate }")
                      delete-menu(
                        v-if="period.user === user || hasPerm('dcis.delete_period')"
                        v-slot="{ on }"
                        :itemName="$t('dcis.periods.deleteItemName')"
                        @confirm="mutate"
                        @cancel="active = false"
                      )
                        v-btn(v-on="on" color="error") {{$t('dcis.periods.actions.delete')}}
                v-col.text-right
                  v-btn(
                    v-if="period.user === user || hasPerm('dcis.change_period')"
                    :disabled="invalid"
                    :loading="loading"
                    type="submit"
                    color="success"
                  ) {{$t('dcis.periods.actions.save')}}
</template>

<script lang="ts">
import { computed, ComputedRef, defineComponent, PropType, ref, Ref, toRefs, useNuxt2Meta, useRouter } from '#app'
import { promiseTimeout } from '@vueuse/core'
import { BreadCrumbsItem } from '~/types/devind'
import {
  ChangePeriodMutationPayload,
  DeletePeriodMutationPayload,
  PeriodType,
  UserType
} from '~/types/graphql'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import { HasPermissionFnType, useAuthStore } from '~/store'
import { useI18n } from '~/composables'
import DeleteMenu from '~/components/common/menu/DeleteMenu.vue'

type ChangePeriodResultMutation = { data: { changePeriod: ChangePeriodMutationPayload } }
type DeletePeriodResultMutation = { data: { deletePeriod: DeletePeriodMutationPayload } }

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

    const period: Ref<PeriodType> = ref<PeriodType>(props.period)
    const name: Ref<string> = ref<string>(props.period.name)
    const multiple: Ref<boolean> = ref<boolean>(props.period.multiple)
    const privately: Ref<boolean> = ref<boolean>(props.period.privately)
    const start: Ref<string> = ref<string>(props.period.start)
    const expiration: Ref<string> = ref<string>(props.period.expiration)

    const chooseStart: Ref<boolean> = ref<boolean>(false)
    const chooseExpiration: Ref<boolean> = ref<boolean>(false)

    const successUpdate: Ref<boolean> = ref<boolean>(false)
    const active: Ref<boolean> = ref<boolean>(false)
    const items: StatusItems[] = [
      { name: 'Подготовка', value: 'preparation' },
      { name: 'Заполнение', value: 'open' },
      { name: 'Сбор закрыт', value: 'close' }
    ]
    const status: Ref<string> = ref<string>(props.period.status)

    const changePeriodDone = ({ data: { changePeriod: { success, period: updatedPeriod } } }: ChangePeriodResultMutation) => {
      if (success) {
        period.value = Object.assign(period.value, updatedPeriod)
        successUpdate.value = true
        promiseTimeout(2000).then(() => (successUpdate.value = false))
      }
    }

    const deletePeriodDone = ({ data: { deletePeriod: { success } } }: DeletePeriodResultMutation) => {
      if (success) {
        router.push(localePath({ name: 'dcis-projects-projectId-periods', params: { projectId: props.period.project.id } }))
      }
    }

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      { text: 'Настройки', to: localePath({ name: 'dcis-periods-periodId-settings' }), exact: true }
    ]))
    return {
      bc,
      name,
      multiple,
      privately,
      start,
      expiration,
      status,
      user,
      hasPerm,
      items,
      chooseStart,
      chooseExpiration,
      active,
      successUpdate,
      changePeriodDone,
      deletePeriodDone
    }
  }
})
</script>
