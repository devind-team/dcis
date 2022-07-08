<template lang="pug">
  mutation-modal-form(
    :header="String($t('dcis.periods.groups.addGroup.header'))"
    :subheader="period.name"
    :button-text="String($t('dcis.periods.groups.addGroup.buttonText'))"
    :mutation="addPeriodGroupMutation"
    :variables="{ name, periodId: period.id }"
    :update="addPeriodGroupUpdate"
    mutation-name="addPeriodGroup"
    errors-in-alert
    @close="close"
  )
    template(#activator="{ on }")
      slot(name="activator" :on="on")
    template(#form)
      validation-provider(
        v-slot="{ errors, valid }"
        :name="String($t('dcis.periods.groups.addGroup.name'))"
        rules="required|min:2"
      )
        v-text-field(
          v-model="name"
          :label="$t('dcis.periods.groups.addGroup.name')"
          :error-messages="errors"
          :success="valid"
          autofocus
        )
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import type { PropType } from '#app'
import { defineComponent, ref } from '#app'
import { AddPeriodGroupMutationPayload, PeriodType } from '~/types/graphql'
import addPeriodGroupMutation from '~/gql/dcis/mutations/project/add_period_group.graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'

export type AddPeriodGroupMutationResult = { data: { addPeriodGroup: Required<AddPeriodGroupMutationPayload> } }
type UpdateFunction = (cache: DataProxy, result: AddPeriodGroupMutationResult) => DataProxy

export default defineComponent({
  components: { MutationModalForm },
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    update: { type: Function as PropType<UpdateFunction>, required: true }
  },
  setup (props) {
    const name = ref<string>('')

    /**
     * Обновление после добавления группы
     * @param cache
     * @param result
     */
    const addPeriodGroupUpdate = (cache: DataProxy, result: AddPeriodGroupMutationResult) => {
      if (result.data.addPeriodGroup.success) {
        props.update(cache, result)
      }
    }

    const close = () => {
      name.value = ''
    }

    return {
      name,
      addPeriodGroupMutation,
      addPeriodGroupUpdate,
      close
    }
  }
})
</script>
