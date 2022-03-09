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
import { PropType } from 'vue'
import { Vue, Component, Prop, Ref } from 'vue-property-decorator'
import { DataTableHeader } from 'vuetify'
import { VDataTable } from 'vuetify/lib'
import { getObjectValueByPath } from 'vuetify/lib/util/helpers'

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

@Component<TreeDataTable>({
  inheritAttrs: false,
  watch: {
    items: {
      immediate: true,
      handler () {
        this.flatItems = this.getFlatItems(this.getItemsWithProps((this.items as Item[])))
      }
    }
  },
  computed: {
    headerSlotName (): string {
      return this.headers ? `header.${this.headers[0].value}` : ''
    },
    outerSlotNames (): string[] {
      return Object.keys(this.$scopedSlots).filter((key: string) =>
        key !== 'body' && !key.startsWith('item') && key !== this.headerSlotName)
    },
    isTree (): boolean {
      return !((this.search && this.search.length) || this.sortBy.length)
    },
    expandedItems (): ItemWithProps[] {
      if (this.isTree) {
        const items: ItemWithProps[] = this.flatItems.filter(this.isItemVisible)
        return this.treeFilter ? items.filter(this.treeFilter) : items
      }
      return this.flatFilter ? this.flatItems.filter(this.flatFilter) : this.flatItems
    },
    hasChildren (): boolean {
      return this.expandedItems.length ? this.expandedItems[0].neighborsHasChildren : false
    }
  }
})
export default class TreeDataTable extends Vue {
  @Prop({ type: Array as PropType<DataTableHeader[] | undefined> })
  readonly headers!: DataTableHeader[] | undefined

  @Prop({ type: Array as PropType<Item[] | undefined> })
  readonly items!: Item[] | undefined

  @Prop({ type: String }) readonly search!: string | undefined
  @Prop({ type: [Boolean, String], default: false }) readonly loading!: boolean | string
  @Prop({ type: Function as PropType<TreeFilter> | undefined }) readonly treeFilter!: TreeFilter | undefined
  @Prop({ type: Function as PropType<FlatFilter | undefined> }) readonly flatFilter!: FlatFilter | undefined

  @Ref() readonly dataTable!: InstanceType<typeof VDataTable> & { colspanAttrs: object | undefined }

  readonly headerSlotName!: string
  readonly outerSlotNames!: string[]
  readonly isTree!: boolean
  readonly expandedItems!: ItemWithProps[]
  readonly hasChildren!: boolean

  flatItems: ItemWithProps[] = []
  sortBy: string | string[] = []
  colspanAttrs: object | undefined = {}
  loadingText: string = ''
  noDataText: string = ''

  async mounted (): Promise<void> {
    await this.$nextTick()
    this.dataTable.$watch('colspanAttrs', (newValue: object | undefined) => {
      this.colspanAttrs = newValue
    }, { immediate: true })
    this.loadingText = this.$vuetify.lang.t(this.dataTable.$props.loadingText)
    this.noDataText = this.$vuetify.lang.t(this.dataTable.$props.noDataText)
  }

  /**
   * Получение значения объекта по строковому пути
   * @param obj
   * @param path
   * @param fallback
   * @return
   */
  getObjectValueByPath (obj: any, path: string, fallback?: any): any {
    return getObjectValueByPath(obj, path, fallback)
  }

  /**
   * Определение показывать элемент или нет
   * @param item
   * @return boolean
   */
  isItemVisible (item: ItemWithProps): boolean {
    if (item.parent) {
      if (item.parent.isExpanded) {
        return this.isItemVisible(item.parent)
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
  getItemScope (headerScope: HeaderScope, item: Item, index: number): ItemName {
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
  expand (expand: (item: Item, v: boolean) => void, item: Item): void {
    expand(item, !item.isExpanded)
    item.isExpanded = !item.isExpanded
  }

  /**
   * Получение стиля для блока раскрытия
   * @param item
   * @return
   */
  getExpandStyle (item: ItemWithProps): { margin: string } {
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
  getHeadersTail (header: DataTableHeader[]): DataTableHeader[] {
    return header.filter((_, index: number) => index !== 0)
  }

  /**
   * Получение классов для ячейки
   * @param header
   * @return
   */
  getTdClasses (header: DataTableHeader): (string | string[] | { [key: string]: boolean | undefined } | undefined)[] {
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
  getItemsWithProps (items: Item[], parent: ItemWithProps | null = null, level: number = 0): ItemWithProps[] {
    const neighborsHasChildren = items.some((item: any) => item.children && item.children.length)
    return items.map((item: any) => {
      const result = { ...item, parent, level, neighborsHasChildren, isExpanded: false }
      if (result.children && result.children.length) {
        result.children = this.getItemsWithProps(result.children, result, level + 1)
      }
      return result
    })
  }

  /**
   * Разбор иерархии элементов в плоскую структуру
   * @param item,
   * @param items
   */
  flatten (item: ItemWithProps, items: ItemWithProps[]): void {
    items.push(item)
    if (item.children && item.children.length) {
      item.children.forEach((child: any) => this.flatten(child, items))
    }
  }

  /**
   * Получение плоской структуры элементов
   * @param items
   * @return
   */
  getFlatItems (items: ItemWithProps[]): ItemWithProps[] {
    const flatItems: ItemWithProps[] = []
    items.forEach((item: ItemWithProps) => {
      this.flatten(item, flatItems)
    })
    return flatItems
  }
}
</script>

<style lang="sass">
  .tree-data-table__expand-block
    width: 24px
  .tree-data-table__expand-block-header
    margin: 0 24px 0 0
</style>
