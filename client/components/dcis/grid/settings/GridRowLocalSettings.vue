<template lang="pug">
v-dialog(v-model="active" width="600" @click:outside="$emit('close')")
  template(#activator="{ on, attrs }")
    slot(name="activator" :on="on" :attrs="attrs")
  validation-observer(v-slot="{ handleSubmit, invalid }" slim)
    form(@submit.prevent="handleSubmit(submit)")
      v-card
        v-card-title
          | {{ String($t('dcis.grid.rowLocalSettings.header')) }}
          v-spacer
          v-btn(@click="$emit('close')" icon)
            v-icon mdi-close
        v-card-text
          validation-provider(
            v-slot="{ errors, valid }"
            :name="String($t('dcis.grid.rowLocalSettings.height'))"
            rules="required|integer|min_value:0"
          )
            v-text-field(
              v-model="height"
              :error-messages="errors"
              :success="valid"
              :label="$t('dcis.grid.rowLocalSettings.height')"
            )
        v-card-actions
          v-btn(color="warning" @click="reset") {{ $t('dcis.grid.rowLocalSettings.reset') }}
          v-spacer
          v-btn(
            :disabled="invalid"
            type="submit"
            color="primary"
          ) {{ $t('dcis.grid.rowLocalSettings.buttonText') }}
</template>

<script lang="ts">
import { defineComponent, PropType } from '#app'
import { RowDimensionType } from '~/types/graphql'

export default defineComponent({
  props: {
    row: { type: Object as PropType<RowDimensionType>, required: true },
    getRowHeight: { type: Function as PropType<(row: RowDimensionType) => number>, required: true }
  },
  setup (props, { emit }) {
    const active = ref<boolean>(false)

    const height = ref<string>(String(props.getRowHeight(props.row)))

    const submit = () => {
      emit('submit', { height: Number(height.value) })
      emit('close')
    }

    const reset = () => {
      emit('reset')
      emit('close')
    }

    return { active, height, submit, reset }
  }
})
</script>
