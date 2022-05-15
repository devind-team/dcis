<template lang="pug">
  v-menu(bottom close-on-content-click)
    template(#activator="{ on: onMenu }")
      v-tooltip(right open-delay="1000")
        template(#activator="{ on: onTooltip, attrs }")
          div(
            v-bind="attrs"
            v-on="onTooltip"
            @contextmenu.prevent="onMenu.click"
            :class="contentClass"
          ) {{ buildRow.rowDimension.name }}
        span {{ t('dcis.grid.rowControl.updatedAt', { updatedAt: dateTimeHM(buildRow.rowDimension.updatedAt) } ) }}
    v-list(dense)
      grid-row-settings(@close="settingsActive = false" :build-row="buildRow")
        template(#activator="{ on }")
          v-list-item(v-on="on")
            v-list-item-icon
              v-icon mdi-cog
            v-list-item-content {{ t('dcis.grid.rowControl.properties') }}
      v-list-item(@click="addRowDimension(buildRow.rowDimension.index - 1)")
        v-list-item-icon
          v-icon mdi-table-row-plus-before
        v-list-item-content {{ t('dcis.grid.rowControl.addRowAbove') }}
      v-list-item(@click="addRowDimension(buildRow.rowDimension.index + 1)")
        v-list-item-icon
          v-icon mdi-table-row-plus-after
        v-list-item-content {{ t('dcis.grid.rowControl.addRowBelow') }}
      v-list-item(
        v-if="buildRow.rowDimension.dynamic"
        @click="addRowDimension(buildRow.rowDimension.children.length ? buildRow.rowDimension.children.at(-1).index + 1 : 1, +buildRow.rowDimension.id)"
      )
        v-list-item-icon
          v-icon mdi-table-row-plus-after
        v-list-item-content {{ t('dcis.grid.rowControl.addChildRow') }}
      v-list-item(@click="deleteRowDimension(+buildRow.rowDimension.id)")
        v-list-item-icon
          v-icon(color="error") mdi-table-row-remove
        v-list-item-content(color="error") {{ t('dcis.grid.rowControl.deleteRow') }}
</template>

<script lang="ts">
import { PropType } from '#app'
import { BuildRowType } from '~/types/grid'
import GridRowSettings from '~/components/dcis/grid/settings/GridRowSettings.vue'

export default defineComponent({
  components: { GridRowSettings },
  props: {
    buildRow: { type: Object as PropType<BuildRowType>, required: true },
    contentClass: { type: Array as PropType<(string | Record<string, boolean>)[]>, default: null }
  },
  setup () {
    const { t } = useI18n()

    const settingsActive = ref<boolean>(false)

    const { dateTimeHM } = useFilters()
    const addRowDimension = (index: number, parentId: number | undefined = undefined) => {
      console.log('addRowDimension', index, parentId)
    }

    const deleteRowDimension = (rowId: number) => {
      console.log('deleteRowDimension', rowId)
    }
    return { t, settingsActive, addRowDimension, deleteRowDimension, dateTimeHM }
  }
})
</script>
