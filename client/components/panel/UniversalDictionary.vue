<template lang="pug">
  left-navigator-container(:bread-crumbs="breadCrumbs" @update-drawer="$emit('update-drawer')")
    template(#header) {{ t(`${queryName}.header`) }}
    v-row(align="center")
      v-col(cols="12" md="6")
        v-text-field(
          v-if="isRelayQuery"
          v-stream:input="searchStream$"
          :placeholder="t('search')"
          prepend-icon="mdi-magnify"
          clearable
        )
        v-text-field(
          v-else
          v-model="search"
          :placeholder="t('search')"
          prepend-icon="mdi-magnify"
          clearable
        )
      v-col.text-right.pr-5(cols="12" md="6") {{ countText }}
    v-row
      v-col
        v-data-table(
          :headers="tableHeaders"
          :items="items"
          :loading="$apollo.queries[queryName].loading"
          :search="!isRelayQuery ? search : undefined"
          dense
          disable-pagination
          hide-default-footer
        )
          template(#item.id="{ item }") {{ isRelayQuery ? $fromGlobalId(item.id).id : item.id }}
          template(v-for="headerValue in booleanHeadersValues" v-slot:[`item.${headerValue}`]="{ item }")
            | {{ getObjectValueByPath(item, headerValue) ? t('yes') : t('no') }}
          template(#footer v-if="isRelayQuery && totalCount > (page * pageSize)")
            v-row
              v-col.text-center
                v-btn(@click="fetchMore" :loading="$apollo.queries[queryName].loading" color="success" outlined)
                  v-icon mdi-download
                  | {{ t('loadMore') }}
          slot(v-for="slot in Object.keys($slots)" :name="slot" :slot="slot")
          template(v-for="slot in tableSlotNames" v-slot:[slot]="scope")
            slot(v-bind="scope" :name="slot")
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'
import { Subject } from 'rxjs'
import { debounceTime, pluck, startWith, tap } from 'rxjs/operators'
import { DataTableHeader } from 'vuetify'
import { getObjectValueByPath } from 'vuetify/lib/util/helpers'
import { DocumentNode } from 'graphql'
import { BreadCrumbsItem } from '~/types/devind'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'

type QueryVariables = {
  first?: number,
  offset?: number,
  [key: string]: any
}
type Header = string | { name: string, value: string }

@Component<UniversalDictionary>({
  components: { LeftNavigatorContainer },
  computed: {
    isRelayQuery () {
      return this.pageSize !== 0
    },
    variables (): QueryVariables | undefined {
      if (!this.isRelayQuery) {
        return this.searchVariables
      }
      const queryVariables: QueryVariables = {
        first: this.pageSize,
        offset: 0
      }
      this.addSearchVariables(queryVariables)
      return queryVariables
    },
    countText (): string {
      if (this.isRelayQuery) {
        return this.t('shownOf', {
          count: this.$data[this.queryName] && this.$data[this.queryName].length,
          totalCount: this.totalCount
        })
      }
      return this.t('totalCount', { count: this.$data[this.queryName] && this.$data[this.queryName].length })
    },
    tableHeaders (): DataTableHeader[] {
      return this.headers.map((header: Header) => {
        if (typeof header === 'string') {
          return {
            text: this.t(`${this.queryName}.tableHeaders.${header}`),
            value: header
          }
        }
        return {
          text: this.t(`${this.queryName}.tableHeaders.${header.name}`),
          value: header.value
        }
      })
    },
    items (): any[] {
      return this.$data[this.queryName]
        ? this.convertItems
          ? this.convertItems(this.$data[this.queryName])
          : this.$data[this.queryName].map((item: any) => {
            const newItem: any = {}
            for (const key in item) {
              if (key in this.convertItem) {
                newItem[key] = this.convertItem[key](item[key])
              } else {
                newItem[key] = item[key]
              }
            }
            return newItem
          })
        : []
    },
    tableSlotNames (): string[] {
      return Object.keys(this.$scopedSlots).filter((key: string) =>
        key !== 'footer' &&
        !['id', ...this.booleanHeaders].find((header: Header) => key === `item.${this.getHeaderValue(header)}`)
      )
    },
    booleanHeadersValues (): string[] {
      return this.booleanHeaders.map((header: Header) => this.getHeaderValue(header))
    }
  },
  domStreams: ['searchStream$'],
  subscriptions () {
    const search$ = this.searchStream$.pipe(
      pluck('event', 'msg'),
      debounceTime(700),
      tap(() => { this.page = 1 }),
      startWith('')
    )
    return { search$ }
  }
})
export default class UniversalDictionary extends Vue {
  @Prop({ required: true, type: Array }) breadCrumbs!: BreadCrumbsItem[]
  @Prop({ required: true, type: Object }) query!: DocumentNode
  @Prop({ required: true, type: String }) queryName!: string
  @Prop({ required: true, type: Array }) headers!: Header[]
  @Prop({ type: Array, default: () => [] }) booleanHeaders!: Header[]
  @Prop({ type: Object, default: () => ({}) }) convertItem!: { [key: string]: Function }
  @Prop({ type: Function }) convertItems!: (items: any) => any | undefined
  @Prop({ type: Number, default: 0 }) pageSize!: number
  @Prop({ type: Object, default: () => ({}) }) searchVariables!: { [key: string]: any }

  isRelayQuery!: boolean
  variables!: QueryVariables | undefined
  countText!: string
  tableHeaders!: DataTableHeader[]
  items!: any[]
  tableSlotNames!: string[]
  booleanHeadersValues!: string[]

  page: number = 1
  totalCount: number = 0
  search$: string = ''
  searchStream$: Subject<any> = new Subject()
  search: string = ''

  created () {
    this.$apollo.addSmartQuery(this.queryName, {
      query: this.query,
      variables: () => this.variables,
      update: this.isRelayQuery
        ? (data: any) => {
            const result = data[this.queryName].edges.map((e: any) => e.node)
            this.totalCount = data[this.queryName].totalCount
            this.page = Math.ceil(result.length / this.pageSize)
            return result
          }
        : undefined
    })
  }

  /**
   * Получение перевода относильно локального пути
   * @param path
   * @param values
   * @return
   */
  t (path: string, values: any = undefined): string {
    return this.$t(`dictionaries.${path}`, values) as string
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
   * Получение значения заголовка
   * @param header
   * @return
   */
  getHeaderValue (header: Header): string {
    if (typeof header === 'string') {
      return header
    }
    return header.value
  }

  /**
   * Добавление переменных поиска
   * @param variables
   */
  addSearchVariables (variables: QueryVariables): void {
    for (const key in this.searchVariables) {
      variables[key] = this.search$ || this.search || this.searchVariables[key]
    }
  }

  /**
   * Догрузка
   */
  async fetchMore (): Promise<void> {
    ++this.page
    const queryVariables: QueryVariables = {
      first: this.pageSize,
      offset: (this.page - 1) * this.pageSize
    }
    this.addSearchVariables(queryVariables)
    await this.$apollo.queries[this.queryName].fetchMore({
      variables: queryVariables,
      updateQuery: (previousResult: any, { fetchMoreResult }: any) => {
        return {
          [this.queryName]: {
            __typename: previousResult[this.queryName].__typename,
            totalCount: fetchMoreResult[this.queryName].totalCount,
            edges: [...previousResult[this.queryName].edges, ...fetchMoreResult[this.queryName].edges]
          }
        }
      }
    })
  }
}
</script>
