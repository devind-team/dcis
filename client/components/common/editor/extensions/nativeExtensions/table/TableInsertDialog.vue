<template lang="pug">
v-dialog(v-model="isTableDialog" width="600")
  template(#activator="{ on }")
    v-tooltip(top)
      template(#activator="{ on: onTooltip, attrs }")
        v-btn(v-on="{ ...on, ...onTooltip }" v-bind="attrs" icon)
          v-icon {{icon}}
      span {{$t('common.richTextEditor.table.insertTable')}}
  validation-observer(v-slot="{ invalid }")
    form(@submit.prevent="onTableInsert")
      v-card
        v-card-title {{$t('common.richTextEditor.table.insertTableHeader')}}
          v-spacer
          v-btn(@click="isTableDialog=false" icon)
            v-icon mdi-close
        v-card-text
          validation-provider(:name="$t('common.richTextEditor.table.cols')" rules="required|min_value:1" v-slot="{ errors, valid }")
            v-text-field(v-model="cols" :label="$t('common.richTextEditor.table.cols')" type="number" :error-messages="errors" :success="valid")
          validation-provider(:name="$t('common.richTextEditor.table.rows')" rules="required|min_value:1" v-slot="{ errors, valid }")
            v-text-field(v-model="rows" :label="$t('common.richTextEditor.table.rows')" type="number" :error-messages="errors" :success="valid")
          v-checkbox(v-model="isHeaderRowEnabled" :label="$t('common.richTextEditor.table.firstRowIsHeader')")
        v-card-actions
          v-spacer
          v-btn(type="submit" :disabled="invalid" color="primary") {{ $t('common.richTextEditor.table.insertTable') }}
</template>

<script lang="ts">
import { defineComponent, PropType, ref } from '#app'
import { Editor } from '@tiptap/core'
import { OnButtonStateChangedType, OnClickType } from '~/components/common/editor/extensions/ExtensionOptionsInterface'

export default defineComponent({
  props: {
    tooltip: { type: String, required: true },
    icon: { type: String, required: true },
    editor: { type: Object as PropType<Editor>, required: true },
    onClick: { type: Function as PropType<OnClickType>, default: () => null },
    isDisabled: { type: Function as PropType<OnButtonStateChangedType>, default: () => null },
    isActive: { type: Function as PropType<OnButtonStateChangedType>, default: () => null },
    isVisible: { type: Function as PropType<OnButtonStateChangedType>, default: () => null }
  },
  setup (props) {
    const isTableDialog = ref(false)
    const isHeaderRowEnabled = ref(true)
    const rows = ref(1)
    const cols = ref(1)

    const onTableInsert = () => {
      props.onClick(props.editor, { rows: rows.value, cols: cols.value, withHeaderRow: isHeaderRowEnabled.value })
      isTableDialog.value = false
    }
    return { isTableDialog, isHeaderRowEnabled, cols, rows, onTableInsert }
  }
})
</script>
