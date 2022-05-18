<template lang="pug">
  mutation-modal-form(
    @close="$emit('close')"
    :header="String(t('dcis.grid.columnSettings.header'))"
    :subheader="String(t('dcis.grid.columnSettings.width', { width }))"
    :mutation="null"
    :variables="{ id: buildColumn.columnDimension.id, hidden, fixed, kind: kind.value, width  }"
    :button-text="String(t('dcis.grid.columnSettings.buttonText'))"
    i18n-path="dcis.grid.columnSettings"
    mutation-name="changeColumnDimension"
  )
    template(#activator="{ on }")
      slot(name="activator" :on="on")
    template(#form)
      v-combobox.mx-1(v-model="kind" :items="kinds" label="Тип")
      //- В разработке
      v-checkbox(v-model="fixed" :label="t('dcis.grid.columnSettings.fix')")
      v-checkbox(v-model="hidden" :label="t('dcis.grid.columnSettings.hide')")
</template>

<script lang="ts">
import { PropType } from '#app'
import { cellKinds } from '~/composables/grid'
import { BuildColumnType } from '~/types/grid'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'

export default defineComponent({
  components: { MutationModalForm },
  props: {
    buildColumn: { type: Object as PropType<BuildColumnType>, required: true },
    getColumnWidth: { type: Function as PropType<(buildColumn: BuildColumnType) => number>, required: true }
  },
  setup (props) {
    const { t } = useI18n()

    const width = computed<number>(() => props.getColumnWidth(props.buildColumn))
    const fixed = ref<boolean>(props.buildColumn.columnDimension.fixed)
    const hidden = ref<boolean>(props.buildColumn.columnDimension.hidden)

    const kind = ref<{ text: string, value: string }>({
      text: t(`dcis.cellKinds.${props.buildColumn.columnDimension.kind}`) as string,
      value: props.buildColumn.columnDimension.kind
    })
    const kinds = computed<{ text: string, value: string }[]>(() => (
      Object.keys(cellKinds).map((k: string) => ({ text: t(`dcis.cellKinds.${k}`) as string, value: k })))
    )

    return { t, width, fixed, hidden, kinds, kind }
  }
})
</script>
