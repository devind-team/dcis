<template lang="pug">
v-dialog(v-model="active" width="600" @click:outside="$emit('close')")
  template(#activator="{ on, attrs }")
    slot(name="activator" :on="on" :attrs="attrs")
  validation-observer(v-slot="{ handleSubmit, invalid }" slim)
    form(@submit.prevent="handleSubmit(submit)")
      v-card
        v-card-title
          | {{ String($t('dcis.grid.columnLocalSettings.header')) }}
          v-spacer
          v-btn(@click="$emit('close')" icon)
            v-icon mdi-close
        v-card-text
          validation-provider(
            v-slot="{ errors, valid }"
            :name="String($t('dcis.grid.columnLocalSettings.width'))"
            rules="required|integer|min_value:0"
          )
            v-text-field(
              v-model="width"
              :error-messages="errors"
              :success="valid"
              :label="$t('dcis.grid.columnLocalSettings.width')"
            )
        v-card-actions
          v-btn(color="warning" @click="reset") {{ $t('dcis.grid.columnLocalSettings.reset') }}
          v-spacer
          v-btn(
            :disabled="invalid"
            type="submit"
            color="primary"
          ) {{ $t('dcis.grid.columnLocalSettings.buttonText') }}
</template>

<script lang="ts">
import { defineComponent, PropType } from '#app'
import { ColumnDimensionType } from '~/types/graphql'

export default defineComponent({
  props: {
    column: { type: Object as PropType<ColumnDimensionType>, required: true },
    getColumnWidth: { type: Function as PropType<(column: ColumnDimensionType) => number>, required: true }
  },
  setup (props, { emit }) {
    const active = ref<boolean>(false)

    const width = ref<string>(String(props.getColumnWidth(props.column)))

    const submit = () => {
      emit('submit', { width: Number(width.value) })
      emit('close')
    }

    const reset = () => {
      emit('reset')
      emit('close')
    }

    return { active, width, submit, reset }
  }
})
</script>
