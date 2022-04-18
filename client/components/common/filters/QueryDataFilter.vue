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
      :multiple="multiple"
      :has-select-all="hasSelectAll"
      :message-container-class="messageContainerClass"
      :title="title"
      :max-width="maxWidth"
      :max-height="maxHeight"
      :no-filtration-message="noFiltrationMessage"
      :multiple-message-function="multipleMessageFunction"
      :search-label="searchLabel"
      :search-function="searchType === 'client' ? searchFunction : undefined"
      :get-name="getName"
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
              v-stream:input="search"
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
import { Class, GetName, Item, MultipleMessageFunction, SearchFunction, Variables } from '~/types/filters'
import ItemsDataFilter from '~/components/common/filters/ItemsDataFilter.vue'
import { useDebounceSearch } from '~/composables'

export default defineComponent({
  components: { ItemsDataFilter },
  inheritAttrs: false,
  model: { prop: 'selectedValue', event: 'update:selectedValue' },
  props: {
    selectedValue: { type: [Object, Array] as PropType<Item | Item[]>, required: true },
    searchLabel: { type: String, required: true },
    searchFunction: { type: Function as PropType<SearchFunction>, default: null },
    searchType: { type: String as PropType<'server' | 'client' | null>, default: null },
    searchKey: { type: [String, Array] as PropType<string | string[]>, default: 'search' },

    itemKey: { type: String, default: null },
    modal: { type: Boolean, default: null },
    multiple: { type: Boolean, default: null },
    hasSelectAll: { type: Boolean, default: null },
    messageContainerClass: { type: [String, Array, Object] as PropType<Class>, default: null },
    title: { type: String, default: null },
    maxWidth: { type: [String, Number], default: null },
    maxHeight: { type: [String, Number], default: null },
    noFiltrationMessage: { type: String, default: null },
    multipleMessageFunction: { type: Function as PropType<MultipleMessageFunction>, default: null },
    getName: { type: Function as PropType<GetName>, default: null },
    variables: { type: Object as PropType<Variables>, default: null },
    first: { type: Number, default: 10 }
  },
  setup (props, { emit }) {
    const { search, debounceSearch } = useDebounceSearch()
    const queryVariables = computed(() => {
      const variables: Variables = props.variables ? { ...props.variables } : {}
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
