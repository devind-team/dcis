<template lang="pug">
v-dialog(v-model="active" width="600")
  template(#activator="{ on, attrs }")
    div(class="mr-1 v-item-group theme--light v-btn-toggle")
      v-btn(
        v-on="on"
        v-bind="attrs"
        :disabled="disabled || !cell"
        :class="[{ 'v-btn--active': cell && cell.aggregation }, themeClass]"
        class="v-btn--has-bg theme--light v-size--default"
        width="40"
        height="40"
      )
        v-icon mdi-sigma
  v-card
    v-card-title {{ t('dcis.grid.sheetToolbar.aggregationTitle') }}
      v-spacer
      v-btn(@click="cancel" icon)
        v-icon mdi-close
    v-card-text
      v-combobox(v-model="aggregationKind" :items="aggregationItems" :label="t('dcis.grid.sheetToolbar.aggregationChoice')")
</template>

<script lang="ts">
import { computed, defineComponent, PropType, ref } from '#app'
import { CellType } from '~/types/graphql'
import { useI18n } from '~/composables'

const aggregationKinds = t => ([
  { text: 'Не задано', value: null },
  ...['sum', 'avg', 'max', 'min'].map(value => ({
    text: t(`dcis.grid.sheetToolbar.aggregationKind.${value}`),
    value
  }))
])

export default defineComponent({
  inheritAttrs: false,
  props: {
    disabled: { type: Boolean, default: true },
    cell: { type: Object as PropType<CellType>, default: null },
    themeClass: { type: String, default: 'theme--light' }
  },
  emits: ['changeKind'],
  setup (props, { emit }) {
    const { t } = useI18n()
    const active = ref<boolean>(false)

    const aggregationItems = aggregationKinds(t)
    const aggregationKind = computed({
      get: () => (aggregationItems.reduce((a, c) => ({ [c.value]: c, ...a }), {})[props.cell?.aggregation]),
      set: value => emit('changeKind', value)
    })
    const cancel = () => {
      emit('close')
      active.value = false
    }

    return { active, cancel, aggregationKind, aggregationItems, t }
  }
})
</script>
