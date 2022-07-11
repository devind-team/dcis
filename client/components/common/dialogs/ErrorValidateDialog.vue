<template lang="pug">
v-dialog(v-model="active" fullscreen)
  template(#activator="{ on }")
    slot(:on="on")
  v-card
    v-card-title {{ $t('common.dialogs.errorValidateDialog.title') }}
      v-spacer
      v-btn(@click="active = false" icon)
        v-icon mdi-close
    v-card-text
      v-text-field(v-model="search" :label="$t('common.dialogs.errorValidateDialog.search')" clearable)
      v-data-table(
        :headers="headers"
        :items="items"
        :search="search"
        disable-pagination
        hide-default-footer
        disable-sort
      )
        template(#item="{ item, index }")
          tr(:style="{ background: !!errorMessages[item.index] ? '#ffE0E0' : '#f0faeb' }")
            td(:key="`index${item.index}`") {{ item.index + 2 }}
            td(
              v-for="header in table.headers"
              :key="`${header}${index}`"
              :class="{ 'error_validate_dialog__cell_error': errorMessages[item.index] && !!errorMessages[item.index][header] }"
            )
              v-tooltip(v-if="errorMessages[item.index] && !!errorMessages[item.index][header]" bottom)
                template(#activator="{ on }")
                  .w-full.h-full.d-flex.align-center(v-on="on") {{ item[header] }}
                span {{ errorMessages[item.index][header].join('. ') }}
              span(v-else) {{ item[header] }}
</template>

<script lang="ts">
import { DataTableHeader } from 'vuetify'
import type { PropType, Ref, ComputedRef } from '#app'
import { ref, computed, defineComponent, toRefs } from '#app'
import { RowFieldErrorType, TableCellType, TableType } from '~/types/graphql'
import { useI18n } from '~/composables'

export default defineComponent({
  props: {
    table: { type: Object as PropType<TableType>, required: true },
    errors: { type: Array as PropType<RowFieldErrorType[]>, required: true }
  },
  setup (props) {
    const { t } = useI18n()
    const { table, errors } = toRefs(props)

    const active: Ref<boolean> = ref<boolean>(false)
    const search: Ref<string | null> = ref<string | null>(null)

    const headers: ComputedRef<DataTableHeader[]> = computed<DataTableHeader[]>(() => ([
      { text: t('common.dialogs.errorValidateDialog.rowNumber'), value: '__index__' },
      ...table.value.headers.map((e: any) => ({
        text: e,
        value: e
      }))
    ]))

    const items: ComputedRef = computed(() => table.value.rows.map((el: any) => (
      el.cells.reduce((a: any, c: TableCellType) => ({ ...a, [c.header]: c.value }), { index: el.index })
    )))

    const errorMessages: ComputedRef = computed(() => (errors.value.reduce((a, c: RowFieldErrorType) => ({
      ...a,
      [c.row]: c.errors.reduce((ar: any, ac: any) => ({ ...ar, [ac.field]: ac.messages }), {})
    }), {})))

    return { active, search, headers, items, errorMessages }
  }
})
</script>

<style lang="sass">
.error_validate_dialog__cell_error
  background: #ff9999
</style>
