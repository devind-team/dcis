<template lang="pug">
base-data-filter(
  :message="message"
  :message-container-class="messageContainerClass"
  :message-container-close="!!selectedItems.length"
  :title="title"
  :modal="modal"
  :fullscreen="fullscreen"
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
    slot(name="search" :search-label="searchLabelComputed" :search-function="searchFunction" :on="searchOn")
      v-card-text.flex-shrink-0(v-if="searchFunction")
        v-text-field(
          v-model="search"
          :label="searchLabelComputed"
          prepend-icon="mdi-magnify"
          hide-details
          clearable
        )
  template(#item-content)
    slot(
      name="items"
      :items="items"
      :searchItems="searchItems"
      :temp-items="tempItems"
      :item-key="itemKey"
      :multiple="multiple"
      :has-select-all="hasSelectAll"
      :get-name="getName"
      :get-selected="getSelected"
      :set-selected="setSelected"
      :all-selected="allSelected"
      :set-all-selected="setAllSelected"
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
import {
  Class,
  GetName,
  Item,
  MessageFunction,
  MultipleMessageFunction,
  SearchFunction,
  SearchOn
} from '~/types/filters'
import BaseDataFilter from '~/components/common/filters/BaseDataFilter.vue'

export default defineComponent({
  components: { BaseDataFilter },
  props: {
    value: { type: [Object, Array] as PropType<Item | Item[]>, default: null },
    items: { type: Array as PropType<Item[]>, required: true },
    itemKey: { type: String, default: 'id' },
    modal: { type: Boolean, default: false },
    fullscreen: { type: Boolean, default: undefined },
    multiple: { type: Boolean, default: false },
    hasSelectAll: { type: Boolean, default: false },
    messageContainerClass: { type: [String, Array, Object] as PropType<Class>, default: null },
    title: { type: String, default: null },
    maxWidth: { type: [String, Number], default: undefined },
    maxHeight: { type: [String, Number], default: undefined },
    messageFunction: { type: Function as PropType<MessageFunction>, default: null },
    noFiltrationMessage: { type: String, default: null },
    multipleMessageFunction: {
      type: Function as PropType<MultipleMessageFunction | null>,
      default: null
    },
    searchLabel: { type: String, default: null },
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
    const { t, tc } = useI18n()

    const searchLabelComputed = computed<string>(() =>
      props.searchLabel || t('common.filters.itemsDataFilter.search')
    )
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
      if (props.messageFunction) {
        return props.messageFunction(selectedItems.value)
      }
      if (selectedItems.value.length === 0) {
        return props.noFiltrationMessage || t('common.filters.itemsDataFilter.noFiltrationMessage')
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

    const clear = () => {
      tempItems.value = props.defaultValue
      emit('clear')
      apply()
    }

    const close = () => {
      tempItems.value = selectedItems.value
      search.value = ''
      emit('close')
    }

    const reset = () => {
      clear()
      tempItems.value = props.defaultValue
      search.value = ''
      emit('reset')
      apply()
    }

    const apply = () => {
      selectedItems.value = tempItems.value
      search.value = ''
      emit('apply')
    }

    const getSelected = (item: Item): boolean => {
      return !!tempItems.value.find(selectedItem => selectedItem[props.itemKey] === item[props.itemKey])
    }
    const setSelected = (item: Item, selected: boolean) => {
      tempItems.value = selected
        ? [...tempItems.value, item]
        : tempItems.value.filter(selectedItem => selectedItem[props.itemKey] !== item[props.itemKey])
    }

    const setAllSelected = (selected: boolean) => {
      allSelected.value = selected
    }

    const defaultMultipleMessageFunction = (name: string, restLength: number): string => {
      return props.multipleMessageFunction
        ? props.multipleMessageFunction(name, restLength)
        : tc('common.filters.itemsDataFilter.multipleMessage', restLength, { name, restLength })
    }

    const select = (items: Item[]) => {
      for (const item of items) {
        setSelected(item, true)
      }
      apply()
    }

    return {
      search,
      searchLabelComputed,
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
      setSelected,
      setAllSelected,
      select
    }
  }
})
</script>
