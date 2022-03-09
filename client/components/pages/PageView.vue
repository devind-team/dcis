<template lang="pug">
  v-data-iterator(:items="pages" :loading="$apollo.queries.pages.loading" disable-pagination hide-default-footer)
    template(#header v-if="allowSearch")
      v-row(align="center")
        v-col(cols="12" md="8")
          v-text-field(v-stream:input="searchStream$" :label="$t('search')" prepend-icon="mdi-magnify" clearable)
        v-col.text-right(v-if="!$apollo.queries.pages.loading && totalCount" cols="12" md="4")
          | {{ $t('pages.components.pageView.showOf', { count: pages.length, totalCount }) }}
          v-btn-toggle.ml-2(v-model="view")
            v-btn(value="grid")
              v-icon mdi-view-grid
            v-btn(value="card")
              v-icon mdi-view-list
    template(#default="{ items }")
      v-row
        v-col(v-if="allowAdd" cols="12")
          add-page-card(:category="category")
      slot(:items="items" :view="view")
    template(#footer)
      v-row(v-if="$apollo.queries.pages.loading")
        v-col.text-center #[v-progress-circular(color="primary" indeterminate)]
    template(#no-data)
      .font-italic(v-if="search$ && search$.length !== 0") {{ $t('pages.components.pageView.noResults') }}
      v-row(v-else)
        v-col
          v-alert(type="info") {{ $t('pages.components.pageView.noPages') }}
        v-col(v-if="allowAdd" v-bind="breakPointsGrid")
          add-page-card(:category="category")
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'
import { fromEvent, Subject } from 'rxjs'
import { debounceTime, distinctUntilChanged, filter, map, pluck, startWith, tap } from 'rxjs/operators'
import {
  CategoryType,
  PagesQueryVariables,
  PageType,
  PageTypeEdge
} from '~/types/graphql'
import pagesQuery from '~/gql/pages/queries/pages.graphql'
import AddPageCard from '~/components/pages/AddPageCard.vue'

@Component<PageView>({
  components: { AddPageCard },
  computed: {
    breakPointsGrid () {
      return {
        cols: 12, md: 6, lg: 6, xl: 4
      }
    },
    pagesVariables () {
      return {
        first: this.pageSize,
        offset: 0,
        categoryId: this.category?.id,
        kindId: this.kindId,
        search: this.search$,
        includePreview: this.includePreview
      }
    }
  },
  watch: {
    view: (value) => {
      window.localStorage.setItem('pageView', value)
    }
  },
  domStreams: ['searchStream$'],
  subscriptions () {
    const search$ = this.searchStream$.pipe(
      pluck('event', 'msg'),
      debounceTime(700),
      distinctUntilChanged(),
      tap(() => { this.page = 1 }),
      startWith('')
    )
    const al$ = fromEvent(document, 'scroll').pipe(
      pluck('target', 'documentElement'),
      debounceTime(100),
      map((target: any) => ({ top: target.scrollTop + window.innerHeight, height: target.offsetHeight })),
      filter(({ top, height }: { top: number, height: number }) => (
        top + 200 >= height &&
        !this.$apollo.queries.pages.loading &&
        this.page * this.pageSize < this.totalCount &&
        this.allowLoading)
      ),
      tap(async () => {
        ++this.page
        await this.fetchMorePages()
      })
    )
    return { al$, search$ }
  },
  apollo: {
    pages: {
      query: pagesQuery,
      variables () {
        return this.pagesVariables
      },
      update ({ pages }: any): PageType[] {
        this.totalCount = pages.totalCount
        this.page = Math.ceil(pages.edges.length / this.pageSize)
        return pages.edges.map((e: PageTypeEdge) => e.node) as PageType[]
      },
      fetchPolicy: 'cache-and-network'
    }
  }
})

export default class PageView extends Vue {
  @Prop({ default: null }) category?: CategoryType | null
  @Prop({ default: null }) kindId?: string | null
  @Prop({ default: 18 }) pageSize!: number
  @Prop({ default: false, type: Boolean }) includePreview!: boolean
  @Prop({ default: false, type: Boolean }) allowSearch!: boolean
  @Prop({ default: false, type: Boolean }) allowLoading!: boolean
  @Prop({ default: false, type: Boolean }) allowAdd!: boolean

  search$: string | null = ''
  searchStream$: Subject<any> = new Subject<any>()

  page: number = 1
  totalCount: number = 0
  view: string = 'grid'

  pagesVariables!: PagesQueryVariables
  pages!: PageType[]

  mounted () {
    const defaultView: string | null = window.localStorage.getItem('pageView')
    if (defaultView !== null) {
      this.view = defaultView
    }
  }

  async fetchMorePages () {
    await this.$apollo.queries.pages.fetchMore({
      variables: {
        first: this.pageSize,
        offset: (this.page - 1) * this.pageSize,
        categoryId: this.category?.id,
        kindId: this.kindId,
        search: this.search$,
        includePreview: this.includePreview
      },
      updateQuery: (previousQueryResult: any, { fetchMoreResult: { pages } }: any) => {
        return {
          pages: {
            __typename: previousQueryResult.pages.__typename,
            totalCount: pages.totalCount,
            edges: [...previousQueryResult.pages.edges, ...pages.edges]
          }
        }
      }
    })
  }
}
</script>
