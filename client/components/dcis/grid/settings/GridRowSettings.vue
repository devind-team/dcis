<template lang="pug">
  mutation-modal-form(
    @close="$emit('close')"
    :header="String(t('dcis.grid.rowSettings.header'))"
    :subheader="String(t('dcis.grid.rowSettings.subheader', { updatedAt: dateTimeHM(row.updatedAt) }))"
    :mutation="null"
    :variables="{ id: row.id, hidden, fixed, dynamic, height }"
    :button-text="String(t('dcis.grid.rowSettings.buttonText'))"
    i18n-path="dcis.grid.rowSettings"
    mutation-name="changeRowDimension"
  )
    template(#activator="{ on }")
      slot(name="activator" :on="on")
    template(#form)
      validation-provider(
        v-slot="{ errors, valid }"
        :name="String(t('dcis.grid.rowSettings.height'))"
        rules="required|integer|min_value:0"
      )
        v-text-field(
          v-model="height"
          :error-messages="errors"
          :success="valid"
          :label="t('dcis.grid.rowSettings.height')"
        )
      v-checkbox(v-model="fixed" :label="t('dcis.grid.rowSettings.fix')" success)
      v-checkbox(v-model="hidden" :label="t('dcis.grid.rowSettings.hide')" success)
      v-checkbox(
        v-model="dynamic"
        :label="t('dcis.grid.rowSettings.makeDynamic')"
        :disabled="row.children.length"
        success
      )
</template>

<script lang="ts">
import { PropType } from '#app'
import { RowDimensionType } from '~/types/graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'

export default defineComponent({
  components: { MutationModalForm },
  props: {
    row: { type: Object as PropType<RowDimensionType>, required: true },
    getRowHeight: { type: Function as PropType<(row: RowDimensionType) => number>, required: true }
  },
  setup (props) {
    const { t } = useI18n()

    const { dateTimeHM } = useFilters()

    const height = ref<number>(props.getRowHeight(props.row))
    const fixed = ref<boolean>(props.row.fixed)
    const hidden = ref<boolean>(props.row.hidden)
    const dynamic = ref<boolean>(props.row.dynamic)

    return { t, dateTimeHM, height, fixed, hidden, dynamic }
  }
})
</script>
