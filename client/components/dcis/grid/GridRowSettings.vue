<template lang="pug">
  mutation-modal-form(
    @close="$emit('close')"
    :header="String(t('dcis.grid.rowSettings.header'))"
    :subheader="row.height ? String(t('dcis.grid.rowSettings.height', { height: row.height })) : undefined"
    :mutation="changeRowDimensionMutation"
    :variables="{ id: row.id, hidden, fixed, dynamic, height: row.height }"
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
import type { BuildRowType } from '~/types/grid-types'
import changeRowDimensionMutation from '~/gql/dcis/mutations/sheet/change_row_dimension.graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'

export default defineComponent({
  components: { MutationModalForm },
  props: {
    row: { type: Object as PropType<BuildRowType>, required: true }
  },
  setup (props) {
    const { t } = useI18n()

    const fixed = ref<boolean>(props.row.fixed)
    const hidden = ref<boolean>(props.row.hidden)
    const dynamic = ref<boolean>(props.row.dynamic)

    return { t, fixed, hidden, dynamic, changeRowDimensionMutation }
  }
})
</script>
