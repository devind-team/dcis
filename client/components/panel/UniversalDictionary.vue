<template lang="pug">
left-navigator-container(:bread-crumbs="breadCrumbs" @update-drawer="$emit('update-drawer')")
  template(#header) {{ $t(`dictionaries.${queryName}.header`) }}
  v-row(align="center")
    v-col(cols="12" md="6")
      v-text-field(
        v-if="isRelayQuery"
        v-model="relaySearch"
        :placeholder="$t('search')"
        prepend-icon="mdi-magnify"
        clearable
      )
      v-text-field(
        v-else
        v-model="search"
        :placeholder="$t('search')"
        prepend-icon="mdi-magnify"
        clearable
      )
    v-col.text-right.pr-5(cols="12" md="6") {{ countText }}
  v-row
    v-col
      v-data-table(
        :headers="tableHeaders"
        :items="items"
        :loading="result.loading.value"
        :search="!isRelayQuery ? search : undefined"
        dense
        disable-pagination
        hide-default-footer
      )
        template(#item.id="{ item }") {{ isRelayQuery ? $fromGlobalId(item.id).id : item.id }}
        template(v-for="headerValue in booleanHeadersValues" v-slot:[`item.${headerValue}`]="{ item }")
          | {{ getObjectValueByPathFunc(item, headerValue) ? $t('yes') : $t('no') }}
        slot(v-for="slot in Object.keys($slots)" :name="slot" :slot="slot")
        template(v-for="slot in tableSlotNames" v-slot:[slot]="scope")
          slot(v-bind="scope" :name="slot")
</template>

<script lang="ts">
import { DataTableHeader } from 'vuetify'
import { getObjectValueByPath } from 'vuetify/lib/util/helpers'
import { DocumentNode } from 'graphql'
import { computed, PropType, useNuxtApp } from '#app'
import { BreadCrumbsItem } from '~/types/devind'
import { useI18n, useCommonQuery, useQueryRelay, useCursorPagination } from '~/composables'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
type QueryVariables = {
  first?: number,
  offset?: number,
  [key: string]: any
}
type Header = string | { name: string, value: string }
export default defineComponent({
  components: { LeftNavigatorContainer },
  props: {
    breadCrumbs: { required: true, type: Array as PropType<BreadCrumbsItem[]> },
    query: { required: true, type: Object as PropType<DocumentNode> },
    queryName: { required: true, type: String },
    headers: { required: true, type: Array as PropType<Header[]> },
    booleanHeaders: { type: Array as PropType<Header[]>, default: () => [] },
    convertItem: { type: Object as PropType<{ [key: string]: Function }>, default: () => ({}) },
    convertItems: { type: Function as PropType<(items: any) => any | undefined>, default: undefined },
    pageSize: { type: Number, default: 0 },
    searchVariables: { type: Object as PropType<{ [key: string]: any }>, default: () => ({}) }
  },
  setup (props) {
    const isRelayQuery = computed<boolean>(() => (props.pageSize !== 0))
    const { search: relaySearch, debounceSearch } = useDebounceSearch()
    const variables = computed<QueryVariables | undefined>(() => {
      if (!isRelayQuery.value) {
        return props.searchVariables
      }
      const queryVariables: QueryVariables = {
        offset: 0,
        search: debounceSearch.value ? debounceSearch.value : ''
      }
      return queryVariables
    })
    const result = isRelayQuery.value
      ? useQueryRelay({
        document: props.query,
        variables: () => variables.value
      },
      {
        isScrollDown: true,
        pagination: useCursorPagination({ pageSize: props.pageSize }),
        fetchScroll: typeof document === 'undefined' ? null : document
      })
      : useCommonQuery({
        document: props.query,
        variables: () => variables.value
      })
    const totalCount = computed<number>(() => 'pagination' in result ? result.pagination.totalCount.value : 0)
    const { t } = useI18n()
    const search = ref<string>('')
    const countText = computed<string>(() => {
      if (isRelayQuery.value) {
        return t('dictionaries.shownOf', {
          count: result.data.value && result.data.value.length,
          totalCount: totalCount.value
        }) as string
      }
      return t('totalCount', { count: result.data.value && result.data.value.length }) as string
    })

    const tableHeaders = computed<DataTableHeader[]>(() => {
      return props.headers.map((header: Header) => {
        if (typeof header === 'string') {
          return {
            text: t(`dictionaries.${props.queryName}.tableHeaders.${header}`) as string,
            value: header
          }
        }
        return {
          text: t(`dictionaries.${props.queryName}.tableHeaders.${header.name}`) as string,
          value: header.value
        }
      })
    })

    const items: unknown = computed(() => {
      return result.data.value
        ? props.convertItems
          ? props.convertItems(result.data.value)
          : result.data.value.map((item: any) => {
            const newItem: any = {}
            for (const key in item) {
              if (key in props.convertItem) {
                newItem[key] = props.convertItem[key](item[key])
              } else {
                newItem[key] = item[key]
              }
            }
            return newItem
          })
        : []
    })
    const tableSlotNames = computed<string[]>(() => {
      return Object.keys(useNuxtApp().$scopedSlots).filter((key: string) =>
        key !== 'footer' &&
        !['id', ...props.booleanHeaders].find((header: Header) => key === `item.${getHeaderValue(header)}`)
      )
    })
    const booleanHeadersValues = computed<string[]>(() => (
      props.booleanHeaders.map((header: Header) => getHeaderValue(header)))
    )
    const getHeaderValue = (header: Header): string => {
      if (typeof header === 'string') {
        return header
      }
      return header.value
    }
    const getObjectValueByPathFunc = (obj: any, path: string, fallback?: any): any => {
      return getObjectValueByPath(obj, path, fallback)
    }
    return {
      isRelayQuery,
      countText,
      tableHeaders,
      items,
      tableSlotNames,
      booleanHeadersValues,
      search,
      getObjectValueByPathFunc,
      result,
      relaySearch
    }
  }
})
</script>
