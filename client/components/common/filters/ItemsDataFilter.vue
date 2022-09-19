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
          :label="$t('common.filters.itemsDataFilter.selectAll')"
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
import type { PropType } from '#app'
import { computed, defineComponent, ref } from '#app'
import { useI18n } from '~/composables'
import { Class, GetName, Item, MultipleMessageFunction, SearchFunction, SearchOn } from '~/types/filters'
import BaseDataFilter from '~/components/common/filters/BaseDataFilter.vue'

export default defineComponent({
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
        return (this as any).$t('common.filters.itemsDataFilter.noFiltrationMessage')
      }
    },
    multipleMessageFunction: {
      type: Function as PropType<MultipleMessageFunction | null>,
      default: null
    },
    searchLabel: {
      type: String,
      default () {
        return (this as any).$t('common.filters.itemsDataFilter.search')
      }
    },
    searchFunction: { type: Function as PropType<SearchFunction>, default: null },
    getName: {
      type: Function as PropType<GetName>,
      default (item: Item) {
        return String(item[(this as any).itemKey])
      }
    },
    defaultValue: { type: [Object, Array], default: () => ([]) }
  },
  setup (props, { emit }) {
    const { tc } = useI18n()

    const search = ref<string>('')
    const tempValue = ref<Item[] | Item>(props.value)

    const searchOn = computed<SearchOn>((): SearchOn => ({
      input: (value: string) => { search.value = value }
    }))

    const selectedItems = computed<Item[]>({
      get: (): Item[] => {
        if (!props.value) { return [] }
        return props.multiple ? props.value : [props.value]
      },
      set: (items: Item[]): void => {
        if (props.multiple) {
          emit('input', items)
        } else if (props.items.length) {
          emit('input', items[items.length - 1])
        } else {
          emit('input', null)
        }
      }
    })
    const tempItems = computed<Item[]>({
      get: (): Item[] => {
        if (!tempValue.value) { return [] }
        return (props.multiple ? tempValue.value : [tempValue.value]) as Item[]
      },
      set: (items: Item[]): void => {
        if (props.multiple) {
          tempValue.value = items
        } else if (props.items.length) {
          tempValue.value = items[items.length - 1]
        } else {
          tempValue.value = null
        }
      }
    })
    const searchItems = computed<Item[]>(() => {
      const items = props.searchFunction
        ? props.items.filter((item: Item) => props.searchFunction(item, search.value || ''))
        : props.items
      return [
        ...items,
        ...tempItems.value.filter(tempItem => !items.find(item => item[props.itemKey] === tempItem[props.itemKey]))
      ]
    })
    const message = computed<string>(() => {
      if (selectedItems.value.length === 0) {
        return props.noFiltrationMessage
      }
      if (selectedItems.value.length === 1) {
        return props.getName(selectedItems.value[0])
      }
      return defaultMultipleMessageFunction(props.getName(selectedItems.value[0]), selectedItems.value.length - 1)
    })

    const allSelected = computed<boolean>({
      get: (): boolean => searchItems.value.length === tempItems.value.length,
      set: (selected: boolean) => {
        tempItems.value = selected ? [...searchItems.value] : []
      }
    })
    /** Очистка фильтра */
    const clear = () => {
      tempItems.value = props.defaultValue
      emit('clear')
      apply()
    }
    /** Закрытие модального окна */
    const close = () => {
      tempItems.value = []
      search.value = ''
      emit('close')
    }
    /** Сброс фильтра */
    const reset = () => {
      clear()
      tempItems.value = props.defaultValue
      search.value = ''
      emit('reset')
      apply()
    }
    /** Применение фильтра */
    const apply = () => {
      selectedItems.value = tempItems.value
      search.value = ''
      emit('apply')
    }
    /**
     * Получение состояния элемента (выбран или не выбран)
     * @param item
     * @return
     */
    const getSelected = (item: Item): boolean => {
      return !!tempItems.value.find(selectedItem => selectedItem[props.itemKey] === item[props.itemKey])
    }
    /**
     * Установка состояния элемента (выбран или не выбран)
     * @param item
     * @param selected
     */
    const setSelected = (item: Item, selected: boolean) => {
      tempItems.value = selected
        ? [...tempItems.value, item]
        : tempItems.value.filter(selectedItem => selectedItem[props.itemKey] !== item[props.itemKey])
    }

    const defaultMultipleMessageFunction = (name: string, restLength: number): string => {
      return props.multipleMessageFunction
        ? props.multipleMessageFunction(name, restLength)
        : tc('common.filters.itemsDataFilter.multipleMessage', restLength, { name, restLength })
    }

    return {
      search,
      tempValue,
      selectedItems,
      tempItems,
      searchItems,
      message,
      allSelected,
      searchOn,
      clear,
      close,
      reset,
      apply,
      getSelected,
      setSelected
    }
  }
})
</script>
