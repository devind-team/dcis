<template lang="pug">
mutation-modal-form(
  @close="close"
  :header="String($t('dcis.periods.actions.addGroup'))"
  :subheader="period.name"
  :button-text="String($t('dcis.periods.addPeriodGroup.buttonText'))"
  :mutation="addPeriodGroup"
  :variables="{ name, periodId: period.id }"
  :update="addPeriodGroupUpdate"
  mutation-name="addPeriodGroup"
  errors-in-alert
  persistent
)
  template(#activator="{ on }")
    slot(name="activator" :on="on")
  template(#form)
    validation-provider(
      :name="String($t('dcis.periods.addPeriodGroup.name'))"
      rules="required|min:2"
      v-slot="{ errors, valid }"
      )
      v-text-field(
        v-model="name"
        :label="$t('dcis.periods.addPeriodGroup.name')"
        :success="valid"
        :error-messages="errors"
        autofocus
      )
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import type { PropType } from '#app'
import { defineComponent, ref } from '#app'
import { AddPeriodGroupMutationPayload, PeriodGroupType, PeriodType } from '~/types/graphql'
import addPeriodGroup from '~/gql/dcis/mutations/project/add_period_group.graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'

export type AddPeriodGroupMutationResult = { data: { addPeriodGroup: AddPeriodGroupMutationPayload } }
type UpdateFunction = (cache: DataProxy | any, result: AddPeriodGroupMutationPayload | any) => DataProxy | any

export default defineComponent({
  components: { MutationModalForm },
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    update: { type: Function as PropType<UpdateFunction>, required: true }
  },
  setup (props) {
    const name = ref<string>('')
    const selectGroup = ref<PeriodGroupType | null>(null)

    /**
     * Обновление после добавления группы
     * @param cache
     * @param result
     */
    const addPeriodGroupUpdate = (cache: DataProxy, result: AddPeriodGroupMutationResult) => {
      const { success } = result.data.addPeriodGroup
      if (success) {
        props.update(cache, result)
      }
    }

    const close = () => {
      name.value = ''
      selectGroup.value = null
    }
    return {
      name,
      selectGroup,
      addPeriodGroup,
      addPeriodGroupUpdate,
      close
    }
  }
})
</script>
