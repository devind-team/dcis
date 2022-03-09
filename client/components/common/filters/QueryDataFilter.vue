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
      v-model="selectedValue"
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
              v-stream:input="searchStream$"
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
import { Vue, Component, Prop, VModel } from 'vue-property-decorator'
import { PropType } from 'vue'
import { Subject } from 'rxjs'
import { debounceTime, distinctUntilChanged, pluck, startWith } from 'rxjs/operators'
import { Class, GetName, Item, MultipleMessageFunction, SearchFunction, Variables } from '~/types/filters'
import ItemsDataFilter from '~/components/common/filters/ItemsDataFilter.vue'

@Component<QueryDataFilter>({
  inheritAttrs: false,
  components: { ItemsDataFilter },
  computed: {
    queryVariables (): Variables | null | undefined {
      const variables: Variables = { ...this.variables } || {}
      if (this.searchType !== 'server') {
        return variables
      }
      if (typeof this.searchKey === 'string') {
        variables[this.searchKey] = this.search$
      } else {
        this.searchKey.forEach((key: string) => {
          variables[key] = this.search$
        })
      }
      if (!this.search$ || this.search$ === '') {
        variables.first = this.first
      }
      return variables
    }
  },
  domStreams: ['searchStream$'],
  subscriptions () {
    const search$ = this.searchStream$.pipe(
      pluck('event', 'msg'),
      debounceTime(700),
      distinctUntilChanged(),
      startWith(null)
    )
    return { search$ }
  }
})
export default class QueryDataFilter extends Vue {
  @Prop({ type: String }) readonly itemKey?: string
  @Prop({ type: Boolean }) readonly modal?: boolean
  @Prop({ type: Boolean }) readonly multiple?: boolean
  @Prop({ type: Boolean }) readonly hasSelectAll?: boolean
  @Prop({ type: [String, Array, Object] as PropType<Class> }) readonly messageContainerClass?: Class
  @Prop({ type: String }) readonly title?: string
  @Prop({ type: [String, Number] }) readonly maxWidth?: string | number
  @Prop({ type: [String, Number] }) readonly maxHeight?: string | number
  @Prop({ type: String }) readonly noFiltrationMessage?: string

  @Prop({ type: Function as PropType<MultipleMessageFunction> })
  readonly multipleMessageFunction?: MultipleMessageFunction

  @Prop({ type: String }) readonly searchLabel!: string
  @Prop({ type: Function as PropType<SearchFunction> }) readonly searchFunction?: SearchFunction
  @Prop({ type: String }) readonly searchType?: 'server' | 'client' | null
  @Prop({ type: [String, Array], default: 'search' }) readonly searchKey!: string | string[]

  @Prop({ type: Function as PropType<GetName> }) readonly getName?: GetName

  @Prop({ type: Object as PropType<Variables> }) readonly variables?: Variables | null
  @Prop({ type: Number, default: 10 }) readonly first!: number

  @VModel({ type: [Object, Array] as PropType<Item | Item[]> })
  readonly selectedValue!: Item | Item[] | null | undefined

  readonly queryVariables!: object

  search$: string | null = null
  searchStream$: Subject<any> = new Subject<any>()
}
</script>
