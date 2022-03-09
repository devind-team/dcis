<template lang="pug">
  v-container
    v-row
      v-col(cols="12" md="8")
        .text-h4.my-5 {{ $t('pages.components.pageNews.news') }}
        page-list
      v-col(cols="12" md="4")
        .text-h4.my-5 {{ $t('pages.components.pageNews.ads') }}
        page-list
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'
import PageGrid from '~/components/pages/views/PageGrid.vue'
import PageList from '~/components/pages/views/PageList.vue'

@Component<PageNews>({
  components: { PageList, PageGrid }
})
export default class PageNews extends Vue { }
</script>
