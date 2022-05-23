<template lang="pug">
  mutation-modal-form(
    @close="$emit('close')"
    :header="String(t('dcis.grid.columnSettings.header'))"
    :subheader="String(t('dcis.grid.columnSettings.subheader', { updatedAt: dateTimeHM(column.updatedAt) }))"
    :mutation="null"
    :variables="{ id: column.id, hidden, fixed, kind: kind.value, width }"
    :button-text="String(t('dcis.grid.columnSettings.buttonText'))"
    i18n-path="dcis.grid.columnSettings"
    mutation-name="changeColumnDimension"
  )
    template(#activator="{ on }")
      slot(name="activator" :on="on")
    template(#form)
      validation-provider(
        v-slot="{ errors, valid }"
        :name="String(t('dcis.grid.columnSettings.width'))"
        rules="required|integer|min_value:0"
      )
        v-text-field(
          v-model="width"
          :error-messages="errors"
          :success="valid"
          :label="t('dcis.grid.columnSettings.width')"
        )
      v-combobox.mx-1(v-model="kind" :items="kinds" :label="t('dcis.grid.columnSettings.kind')" success)
      //- В разработке
      v-checkbox(v-model="fixed" :label="t('dcis.grid.columnSettings.fix')" success)
      v-checkbox(v-model="hidden" :label="t('dcis.grid.columnSettings.hide')" success)
</template>

<script lang="ts">
import { PropType } from '#app'
import { ColumnDimensionType } from '~/types/graphql'
import { cellKinds } from '~/composables/grid'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'

export default defineComponent({
  components: { MutationModalForm },
  props: {
    column: { type: Object as PropType<ColumnDimensionType>, required: true },
    getColumnWidth: { type: Function as PropType<(column: ColumnDimensionType) => number>, required: true }
  },
  setup (props) {
    const { t } = useI18n()

    const { dateTimeHM } = useFilters()

    const width = ref<number>(props.getColumnWidth(props.column))
    const fixed = ref<boolean>(props.column.fixed)
    const hidden = ref<boolean>(props.column.hidden)

    const kind = ref<{ text: string, value: string }>({
      text: t(`dcis.cellKinds.${props.column.kind}`) as string,
      value: props.column.kind
    })
    const kinds = computed<{ text: string, value: string }[]>(() => (
      Object.keys(cellKinds).map((k: string) => ({ text: t(`dcis.cellKinds.${k}`) as string, value: k })))
    )

    return { t, dateTimeHM, width, fixed, hidden, kinds, kind }
  }
})
</script>
