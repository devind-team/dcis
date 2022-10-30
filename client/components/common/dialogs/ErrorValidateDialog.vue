<template lang="pug">
v-dialog(v-model="active" fullscreen)
  template(#activator="{ on }")
    slot(:on="on")
  v-card
    v-card-title {{ title ? title : $t('common.dialogs.errorValidateDialog.title') }}
      v-spacer
      v-btn(@click="active = false" icon)
        v-icon mdi-close
    v-card-text
      v-text-field(
        v-if="showSearch"
        v-model="search"
        :label="$t('common.dialogs.errorValidateDialog.search')"
        clearable
      )
      v-data-table(
        :headers="headers"
        :items="rows"
        :search="search"
        disable-pagination
        hide-default-footer
        disable-sort
      )
        template(#item="{ item, index }")
          tr(:style="rowStyle(item)")
            td(:key="`index${item.index}`") {{ item.index + 1 }}
            td(
              v-for="header in table.headers"
              :key="`${header}${index}`"
              :class="{ 'error_validate_dialog__cell_error': errorMessages[item.index] && !!errorMessages[item.index][header] }"
            )
              v-tooltip(
                v-if="mode === ErrorValidateDialogMode.TOOLTIP && errorMessages[item.index] && !!errorMessages[item.index][header]"
                bottom
              )
                template(#activator="{ on }")
                  .w-full.h-full.d-flex.align-center(v-on="on") {{ item[header] }}
                span {{ errorMessages[item.index][header].join('. ') }}
              span(v-else) {{ item[header] }}
</template>

<script lang="ts">
import { DataTableHeader } from 'vuetify'
import type { PropType } from '#app'
import { ref, computed, defineComponent, toRefs } from '#app'
import { RowFieldErrorType, TableType, TableRowType, TableCellType } from '~/types/graphql'
import { useI18n } from '~/composables'

export enum ErrorValidateDialogMode {
  TOOLTIP,
  TABLE
}

export default defineComponent({
  props: {
    table: { type: Object as PropType<TableType>, required: true },
    errors: { type: Array as PropType<RowFieldErrorType[]>, required: true },
    mode: { type: Number as PropType<ErrorValidateDialogMode>, default: ErrorValidateDialogMode.TOOLTIP },
    title: { type: String, default: null },
    showSearch: { type: Boolean, default: true }
  },
  setup (props) {
    const { t } = useI18n()
    const { table, errors } = toRefs(props)

    const active = ref<boolean>(false)
    const search = ref<string | null>(null)

    const headers = computed<DataTableHeader[]>(() => ([
      { text: t('common.dialogs.errorValidateDialog.rowNumber'), value: '__index__' },
      ...table.value.headers.map((e: any) => ({
        text: e,
        value: e
      }))
    ]))

    const rows = computed<TableRowType[]>(() => table.value.rows.map((el: any) => (
      el.cells.reduce((a: any, c: TableCellType) => ({ ...a, [c.header]: c.value }), { index: el.index })
    )))

    const errorMessages = computed(() => (errors.value.reduce((a, c: RowFieldErrorType) => ({
      ...a,
      [c.row]: c.errors.reduce((ar: any, ac: any) => ({ ...ar, [ac.field]: ac.messages }), {})
    }), {})))

    const rowStyle = (row: TableRowType) => {
      if (props.mode === ErrorValidateDialogMode.TOOLTIP) {
        return { backgroundColor: errorMessages[row.index] ? '#ffE0E0' : '#f0faeb' }
      }
      return {}
    }

    return { ErrorValidateDialogMode, active, search, headers, rows, errorMessages, rowStyle }
  }
})
</script>

<style lang="sass">
.error_validate_dialog__cell_error
  background: #ff9999
</style>
