<template lang="pug">
  base-data-filter(
    :message="message"
    :message-container-class="messageContainerClass"
    :message-container-close="!!selectedItems.length"
    :title="title"
    :modal="modal"
    :max-width="maxWidth"
    :max-height="maxHeight"
    @clear="clear"
    @close="close"
    @reset="reset"
    @apply="apply"
  )
    template(#message="message")
      slot(name="message" v-bind="message")
    template(#title="title")
      slot(name="title" v-bind="title")
    template(#subtitle)
      slot(name="subtitle")
    template(#fixed-content)
      slot(name="search" :search-label="searchLabel" :search-function="searchFunction" :on="searchOn")
        v-card-text.flex-shrink-0(v-if="searchFunction")
          v-text-field(
            v-model="search"
            :label="searchLabel"
            prepend-icon="mdi-magnify"
            hide-details
            clearable
          )
    template(#item-content)
      slot(
        name="items"
        :items="items"
        :searchItems="searchItems"
        :item-key="itemKey"
        :multiple="multiple"
        :has-select-all="hasSelectAll"
        :get-name="getName"
        :get-selected="getSelected"
        :set-selected="setSelected"
      )
        template(v-if="multiple")
          v-checkbox.my-2(
            v-if="hasSelectAll && searchItems.length"
            v-model="allSelected"
            :label="t('selectAll')"
            hide-details
          )
          template(v-for="item in searchItems")
            slot(
              name="item"
              :item="item"
              :get-name="getName"
              :is-selected="getSelected(item)"
              :change="setSelected.bind(this, item)"
            )
              v-checkbox.my-2(
                :key="item[itemKey]"
                :input-value="getSelected(item)"
                :label="getName(item)"
                hide-details
                @change="setSelected(item, $event)"
              )
        v-radio-group.my-2(v-else v-model="tempValue" hide-details)
          template(v-for="item in searchItems")
            slot(
              name="item"
              :item="item"
              :get-name="getName"
              :is-selected="getSelected(item)"
              :change="setSelected.bind(this, item)"
            )
              v-radio(:key="item[itemKey]" :value="item" :label="getName(item)")
    template(#actions="actions")
      slot(name="actions" v-bind="actions")
</template>

<script lang="ts">
import Vue, { PropType } from 'vue'
import { Class, GetName, Item, MultipleMessageFunction, SearchFunction, SearchOn } from '~/types/filters'
import BaseDataFilter from '~/components/common/filters/BaseDataFilter.vue'

export default Vue.extend<any, any, any, any>({
  components: { BaseDataFilter },
  props: {
    value: { type: [Object, Array] as PropType<Item | Item[]>, default: null },
    items: { type: Array as PropType<Item[]>, required: true },
    itemKey: { type: String, default: 'id' },
    modal: { type: Boolean, default: false },
    multiple: { type: Boolean, default: false },
    hasSelectAll: { type: Boolean, default: false },
    messageContainerClass: { type: [String, Array, Object] as PropType<Class>, default: null },
    title: { type: String, default: null },
    maxWidth: { type: [String, Number], default: undefined },
    maxHeight: { type: [String, Number], default: undefined },
    noFiltrationMessage: {
      type: String,
      default () {
        return (this as any).$options.methods.t.call(this, 'noFiltrationMessage')
      }
    },
    multipleMessageFunction: {
      type: Function as PropType<MultipleMessageFunction>,
      default (name: string, restLength: number): string {
        return (this as any).$tc('common.filters.itemsDataFilter.multipleMessage', restLength, { name, restLength })
      }
    },
    searchLabel: {
      type: String,
      default () {
        return (this as any).$options.methods.t.call(this, 'search')
      }
    },
    searchFunction: { type: Function as PropType<SearchFunction>, default: null },
    getName: {
      type: Function as PropType<GetName>,
      default (item: Item) {
        return String(item[(this as any).itemKey])
      }
    }
  },
  data () {
    return {
      search: '',
      tempValue: this.value
    }
  },
  computed: {
    message (): string {
      if (this.selectedItems.length === 0) {
        return this.noFiltrationMessage
      }
      if (this.selectedItems.length === 1) {
        return this.getName(this.selectedItems[0])
      }
      return this.multipleMessageFunction(this.getName(this.selectedItems[0]), this.selectedItems.length - 1)
    },
    searchItems (): Item[] {
      const items = this.searchFunction
        ? this.items.filter((item: Item) => this.searchFunction!(item, this.search || ''))
        : this.items
      return [
        ...items,
        ...this.tempItems.filter(tempItem => !items.find(item => item[this.itemKey] === tempItem[this.itemKey]))
      ]
    },
    selectedItems: {
      get (): Item[] {
        if (!this.value) {
          return []
        }
        if (this.multiple) {
          return this.value as Item[]
        }
        return [this.value as Item]
      },
      set (items: Item[]): void {
        if (this.multiple) {
          this.$emit('input', items)
        } else if (this.items.length) {
          this.$emit('input', items[items.length - 1])
        } else {
          this.$emit('input', null)
        }
      }
    },
    tempItems: {
      get (): Item[] {
        if (!this.tempValue) {
          return []
        }
        if (this.multiple) {
          return this.tempValue as Item[]
        }
        return [this.tempValue as Item]
      },
      set (items: Item[]): void {
        if (this.multiple) {
          this.tempValue = items
        } else if (this.items.length) {
          this.tempValue = items[items.length - 1]
        } else {
          this.tempValue = null
        }
      }
    },
    allSelected: {
      get (): boolean {
        return this.searchItems.length === this.tempItems.length
      },
      set (selected: boolean): void {
        this.tempItems = selected ? [...this.searchItems] : []
      }
    },
    searchOn (): SearchOn {
      return {
        input: (value: string) => {
          this.search = value
        }
      }
    }
  },
  methods: {
    /**
     * Получение перевода относильно локального пути
     * @param path
     * @param values
     * @return
     */
    t (path: string, values?: any): string {
      return this.$t(`common.filters.itemsDataFilter.${path}`, values) as string
    },
    /**
     * Очистка фильтра
     */
    clear (): void {
      this.selectedItems = []
      this.$emit('clear')
    },
    /**
     * Закрытие модального окна
     */
    close (): void {
      this.tempItems = []
      this.search = ''
      this.$emit('close')
    },
    /**
     * Сброс фильтра
     */
    reset (): void {
      this.clear()
      this.tempItems = []
      this.search = ''
      this.$emit('reset')
    },
    /**
     * Применение фильтра
     */
    apply (): void {
      this.selectedItems = this.tempItems
      this.search = ''
      this.$emit('apply')
    },
    /**
     * Получение состояния элемента (выбран или не выбран)
     * @param item
     * @return
     */
    getSelected (item: Item): boolean {
      return !!this.tempItems.find(selectedItem => selectedItem[this.itemKey] === item[this.itemKey])
    },
    /**
     * Установка состояния элемента (выбран или не выбран)
     * @param item
     * @param selected
     */
    setSelected (item: Item, selected: boolean): void {
      if (selected) {
        this.tempItems = [...this.tempItems, item]
      } else {
        this.tempItems = this.tempItems.filter(selectedItem => selectedItem[this.itemKey] !== item[this.itemKey])
      }
    }
  }
})
</script>
