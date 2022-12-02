<template lang="pug">
apollo-query(
  v-slot="{ result: { data, loading } }"
  v-bind="$attrs"
  v-on="$listeners"
  :variables="queryVariables"
  notify-on-network-status-change
  tag
)
  items-data-filter(
    v-model="sv"
    :items="data || []"
    :item-key="itemKey"
    :modal="modal"
    :fullscreen="fullscreen"
    :multiple="multiple"
    :has-select-all="hasSelectAll"
    :disabled="disabled"
    :message-container-class="messageContainerClass"
    :title="title"
    :max-width="maxWidth"
    :max-height="maxHeight"
    :message-function="messageFunction"
    :no-filtration-message="noFiltrationMessage"
    :multiple-message-function="multipleMessageFunction"
    :search-label="searchLabel"
    :search-function="searchType === 'client' ? searchFunction : undefined"
    :get-name="getName"
    @active-changed="$emit('active-changed', $event)"
    @clear="$emit('clear')"
    @close="$emit('close')"
    @reset="$emit('reset')"
    @apply="$emit('apply')"
  )
    template(#message="message")
      slot(name="message" v-bind="message")
    template(#title="title")
      slot(name="title" v-bind="title")
    template(#subtitle)
      slot(name="subtitle")
    template(#search="{ searchLabel, searchFunction, on }")
      slot(
        name="search"
        :search-label="searchLabel"
        :search-function="searchFunction"
        :on="on"
        :loading="loading"
        :search-type="searchType"
        :search-key="searchKey"
      )
        v-card-text.flex-shrink-0(v-if="searchType")
          v-text-field(
            v-model="search"
            v-on="on"
            :label="searchLabel"
            :loading="loading"
            prepend-icon="mdi-magnify"
            hide-details
            clearable
          )
    template(#items="items")
      slot(name="items" v-bind="items")
    template(#item="item")
      slot(name="item" v-bind="item")
    template(#actions="actions")
      slot(name="actions" v-bind="actions")
</template>

<script lang="ts">
import { useVModel } from '@vueuse/core'
import type { PropType } from '#app'
import { computed, defineComponent } from '#app'
import {
  Class,
  GetName,
  Item,
  MessageFunction,
  MultipleMessageFunction,
  SearchFunction,
  Variables
} from '~/types/filters'
import ItemsDataFilter from '~/components/common/filters/ItemsDataFilter.vue'
import { useDebounceSearch } from '~/composables'

export default defineComponent({
  components: { ItemsDataFilter },
  inheritAttrs: false,
  model: { prop: 'selectedValue', event: 'update:selectedValue' },
  props: {
    selectedValue: { type: [Object, Array] as PropType<Item | Item[]>, default: null },
    searchLabel: { type: String, default: undefined },
    searchFunction: { type: Function as PropType<SearchFunction>, default: undefined },
    searchType: { type: String as PropType<'server' | 'client' | null>, default: null },
    searchKey: { type: [String, Array] as PropType<string | string[]>, default: 'search' },

    itemKey: { type: String, default: undefined },
    modal: { type: Boolean, default: false },
    fullscreen: { type: Boolean, default: undefined },
    multiple: { type: Boolean, default: undefined },
    hasSelectAll: { type: Boolean, default: undefined },
    disabled: { type: Boolean, default: false },
    messageContainerClass: { type: [String, Array, Object] as PropType<Class>, default: undefined },
    title: { type: String, default: undefined },
    maxWidth: { type: [String, Number], default: undefined },
    maxHeight: { type: [String, Number], default: undefined },
    messageFunction: { type: Function as PropType<MessageFunction>, default: undefined },
    noFiltrationMessage: { type: String, default: undefined },
    multipleMessageFunction: { type: Function as PropType<MultipleMessageFunction>, default: undefined },
    getName: { type: Function as PropType<GetName>, default: undefined },
    variables: { type: Object as PropType<Variables>, default: undefined },
    first: { type: Number, default: 10 }
  },
  setup (props, { emit }) {
    const { search, debounceSearch } = useDebounceSearch()
    const queryVariables = computed(() => {
      const { variables = { } } = props
      if (props.searchType !== 'server') {
        return variables
      }
      if (typeof props.searchKey === 'string') {
        variables[props.searchKey] = debounceSearch.value
      } else {
        for (const key of props.searchKey) {
          variables[key] = debounceSearch.value
        }
      }
      if (!debounceSearch.value || debounceSearch.value === '') {
        variables.first = props.first
      }
      return variables
    })
    const sv = useVModel(props, 'selectedValue', emit)
    return { search, queryVariables, sv }
  }
})
</script>
