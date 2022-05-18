<template lang="pug">
  mutation-modal-form(
    @close="$emit('close')"
    :header="String(t('dcis.grid.rowSettings.header'))"
    :subheader="String(t('dcis.grid.rowSettings.height', { height: buildRow.height }))"
    :mutation="null"
    :variables="{ id: buildRow.rowDimension.id, hidden, fixed, dynamic, height: buildRow.rowDimension.height }"
    :button-text="String(t('dcis.grid.rowSettings.buttonText'))"
    i18n-path="dcis.grid.rowSettings"
    mutation-name="changeRowDimension"
  )
    template(#activator="{ on }")
      slot(name="activator" :on="on")
    template(#form)
      v-checkbox(v-model="fixed" :label="t('dcis.grid.rowSettings.fix')")
      v-checkbox(v-model="hidden" :label="t('dcis.grid.rowSettings.hide')")
      v-checkbox(v-model="dynamic" :label="t('dcis.grid.rowSettings.makeDynamic')")
</template>

<script lang="ts">
import type { PropType } from '#app'
import type { BuildRowType } from '~/types/grid'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'

export default defineComponent({
  components: { MutationModalForm },
  props: {
    buildRow: { type: Object as PropType<BuildRowType>, required: true }
  },
  setup (props) {
    const { t } = useI18n()

    const fixed = ref<boolean>(props.buildRow.rowDimension.fixed)
    const hidden = ref<boolean>(props.buildRow.rowDimension.hidden)
    const dynamic = ref<boolean>(props.buildRow.rowDimension.dynamic)

    return { t, fixed, hidden, dynamic }
  }
})
</script>
