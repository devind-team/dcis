<template lang="pug">
  v-data-table(
    ref="dataTable"
    v-bind="{ ...$attrs, headers, items: expandedItems, search, loading }"
    v-on="$listeners"
    :sort-by.sync="sortBy"
    @current-items="items => $emit('items', items, expandedItems, flatItems)"
  )
    template(v-if="isTree && hasChildren" v-slot:[headerSlotName])
      .inline-block
        .d-flex.align-baseline.h-full
          .tree-data-table__expand-block.tree-data-table__expand-block-header
          | {{ headers[0].text }}
    template(#body="bodyScope")
      tbody
        tr.v-data-table__empty-wrapper(v-if="bodyScope.items.length === 0 && loading")
          td(v-bind="colspanAttrs") {{ loadingText }}
        tr.v-data-table__empty-wrapper(v-else-if="bodyScope.items.length === 0")
          td(v-bind="colspanAttrs") {{ noDataText }}
        tr(
          v-else
          v-for="item in bodyScope.items"
          :class="[item.itemClass]"
          @click="$emit('click:row', item)"
          @contextmenu="$emit('contextmenu:row', $event)"
          @dbclick="$emit('dblclick:row', $event)"
        )
          td(:class="getTdClasses(bodyScope.headers[0])" :width="bodyScope.headers[0].width")
            .d-flex.align-center.h-full
              v-icon.v-data-table__expand-icon(
                v-if="item.children && item.children.length && isTree"
                :class="{ 'v-data-table__expand-icon--active': bodyScope.isExpanded(item) }"
                :style="getExpandStyle(item)"
                @click="expand(bodyScope.expand, item)"
              ) {{ $vuetify.icons.values.expand }}
              .tree-data-table__expand-block(v-else-if="isTree && hasChildren" :style="getExpandStyle(item)")
              | {{ item[bodyScope.headers[0].value] }}
          td(
            v-for="(header, headerIndex) in getHeadersTail(bodyScope.headers)"
            :width="header.width"
            :class="getTdClasses(header)"
          )
            slot(:name="`item.${header.value}`" v-bind="getItemScope(bodyScope, item, headerIndex)")
              | {{ getObjectValueByPath(item, header.value) }}
    slot(v-for="slot in Object.keys($slots)" :name="slot" :slot="slot")
    template(v-for="slot in outerSlotNames" v-slot:[slot]="scope")
      slot(v-bind="scope" :name="slot")
</template>

<script lang="ts">
import { defineComponent, PropType, ref, computed, onMounted, nextTick, watch } from '#app'
import { DataTableHeader } from 'vuetify'
import { VDataTable } from 'vuetify/lib'
import { getObjectValueByPath } from 'vuetify/lib/util/helpers'
import { useVuetify } from '~/composables'

type Item = { [key: string]: any, children?: Item[] | null }
type HeaderScope = {
  isMobile: boolean,
  item: Item,
  headers: DataTableHeader[],
  value: any
}
type ItemName = {
  isMobile: boolean,
  item: Item,
  header: DataTableHeader,
  value: any
}
export type ItemWithProps = Omit<Item, 'children'> & {
  children: ItemWithProps[]
  parent: ItemWithProps | null,
  level: number,
  neighborsHasChildren: boolean,
  isExpanded: boolean,
  isVisible: boolean
}
export type TreeFilter = (item: ItemWithProps) => boolean
export type FlatFilter = (item: ItemWithProps) => boolean

export default defineComponent({
  inheritAttrs: false,
  props: {
    headers: { type: Array as PropType<DataTableHeader[] | undefined>, default: () => undefined },
    items: { type: Array as PropType<Item[] | undefined>, default: () => undefined },
    search: { type: String, default: () => undefined },
    loading: { type: [Boolean, String], default: false },
    treeFilter: { type: Function as PropType<TreeFilter> | undefined, default: undefined },
    flatFilter: { type: Function as PropType<FlatFilter | undefined>, default: undefined }
  },
  setup (props, { slots }) {
    const { vuetify } = useVuetify()

    const dataTable = ref<InstanceType<typeof VDataTable> & { colspanAttrs: object | undefined }>()

    const flatItems = ref<ItemWithProps[]>([])
    const sortBy = ref<string | string[]>([])
    const colspanAttrs = ref<object | undefined>({})
    const loadingText = ref('')
    const noDataText = ref('')

    const headerSlotName = computed(() => {
      return props.headers ? `header.${props.headers[0].value}` : ''
    })

    const outerSlotNames = computed(() => {
      return Object.keys(slots).filter((key: string) => // todo: scopedSlots -> slots??
        key !== 'body' && !key.startsWith('item') && key !== headerSlotName.value)
    })
    const isTree = computed(() => {
      return !((props.search && props.search.length) || sortBy.value.length)
    })
    const expandedItems = computed(() => {
      if (isTree.value) {
        const items: ItemWithProps[] = flatItems.value.filter(isItemVisible)
        return props.treeFilter ? items.filter(props.treeFilter) : items
      }
      return props.flatFilter ? flatItems.value.filter(props.flatFilter) : flatItems.value
    })
    const hasChildren = computed(() => {
      return expandedItems.value.length ? expandedItems.value[0].neighborsHasChildren : false
    })

    /**
     * Определение показывать элемент или нет
     * @param item
     * @return boolean
     */
    const isItemVisible = (item: ItemWithProps): boolean => {
      if (item.parent) {
        if (item.parent.isExpanded) {
          return isItemVisible(item.parent)
        }
        return false
      }
      return true
    }

    /**
     * Получение данных для слота item.
     * @param headerScope
     * @param item
     * @param index
     * @return
     */
    const getItemScope = (headerScope: HeaderScope, item: Item, index: number): ItemName => {
      return {
        isMobile: headerScope.isMobile,
        item,
        header: headerScope.headers[index],
        value: item[headerScope.headers[index].value]
      }
    }

    /**
     * Раскрытие элемента
     * @param expand
     * @param item
     */
    const expand = (expand: (item: Item, v: boolean) => void, item: Item): void => {
      expand(item, !item.isExpanded)
      item.isExpanded = !item.isExpanded
    }

    /**
     * Получение стиля для блока раскрытия
     * @param item
     * @return
     */
    const getExpandStyle = (item: ItemWithProps): { margin: string } => {
      const marginRight = item.neighborsHasChildren
        ? 24 * item.level
        : 24 * (item.level - 1) >= 0
          ? 24 * (item.level - 1)
          : 0
      return {
        margin: `0 24px 0 ${marginRight}px`
      }
    }

    /**
     * Получение заголовков кроме первого
     * @param header
     * @return
     */
    const getHeadersTail = (header: DataTableHeader[]): DataTableHeader[] => {
      return header.filter((_, index: number) => index !== 0)
    }

    /**
     * Получение классов для ячейки
     * @param header
     * @return
     */
    const getTdClasses = (header: DataTableHeader): (string | string[] | { [key: string]: boolean | undefined } | undefined)[] => {
      return [
        `text-${header.align || 'start'}`,
        header.cellClass,
        { 'v-data-table__divider': header.divider }
      ]
    }

    /**
     * Получение элементов с дополнительными свойствами
     * @param items
     * @param parent
     * @param level
     * @return
     */
    const getItemsWithProps = (items: Item[], parent: ItemWithProps | null = null, level: number = 0): ItemWithProps[] => {
      const neighborsHasChildren = items.some((item: any) => item.children && item.children.length)
      return items.map((item: any) => {
        const result = { ...item, parent, level, neighborsHasChildren, isExpanded: false }
        if (result.children && result.children.length) {
          result.children = getItemsWithProps(result.children, result, level + 1)
        }
        return result
      })
    }

    /**
     * Разбор иерархии элементов в плоскую структуру
     * @param item,
     * @param items
     */
    const flatten = (item: ItemWithProps, items: ItemWithProps[]): void => {
      items.push(item)
      if (item.children && item.children.length) {
        item.children.forEach((child: any) => flatten(child, items))
      }
    }

    /**
     * Получение плоской структуры элементов
     * @param items
     * @return
     */
    const getFlatItems = (items: ItemWithProps[]): ItemWithProps[] => {
      const flatItems: ItemWithProps[] = []
      items.forEach((item: ItemWithProps) => {
        flatten(item, flatItems)
      })
      return flatItems
    }
    onMounted(async () => {
      await nextTick()
      dataTable.value.$watch('colspanAttrs', (newValue: object | undefined) => {
        colspanAttrs.value = newValue
      }, { immediate: true })
      loadingText.value = vuetify.lang.t(dataTable.value.$props.loadingText)
      noDataText.value = vuetify.lang.t(dataTable.value.$props.noDataText)
    })

    watch(
      props.items,
      () => {
        flatItems.value = getFlatItems(getItemsWithProps((props.items as Item[])))
      },
      { immediate: true }
    )
    return {
      expandedItems,
      sortBy,
      flatItems,
      loadingText,
      isTree,
      hasChildren,
      colspanAttrs,
      noDataText,
      outerSlotNames,
      getTdClasses,
      getExpandStyle,
      getObjectValueByPath,
      expand,
      getHeadersTail,
      getItemScope
    }
  }
})
</script>

<style lang="sass">
  .tree-data-table__expand-block
    width: 24px
  .tree-data-table__expand-block-header
    margin: 0 24px 0 0
</style>
