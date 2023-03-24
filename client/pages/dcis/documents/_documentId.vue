<template lang="pug">
div
  left-navigator-driver(v-model="drawer" :items="links")
  v-progress-circular(v-if="loading" color="primary" indeterminate)
  nuxt-child(v-else :breadCrumbs="bc" :document="activeDocument" @update-drawer="drawer = !drawer")
</template>

<script lang="ts">
import { computed, defineComponent, inject, onUnmounted, PropType, ref, useRoute } from '#app'
import { toGlobalId } from '~/services/graphql-relay'
import { useCommonQuery, useI18n } from '~/composables'
import { BreadCrumbsItem, LinksType } from '~/types/devind'
import type { DocumentQuery, DocumentQueryVariables } from '~/types/graphql'
import documentQuery from '~/gql/dcis/queries/document.graphql'
import LeftNavigatorDriver from '~/components/common/grid/LeftNavigatorDriver.vue'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'

export default defineComponent({
  components: { LeftNavigatorDriver, BreadCrumbs },
  props: {
    breadCrumbs: { required: true, type: Array as PropType<BreadCrumbsItem[]> }
  },
  setup (props) {
    const { t, localePath } = useI18n()
    const route = useRoute()

    const {
      data: activeDocument,
      loading
    } = useCommonQuery<DocumentQuery, DocumentQueryVariables>({
      document: documentQuery,
      variables: () => ({
        documentId: route.params.documentId
      })
    })

    const drawer = ref<boolean>(false)
    const links = computed<LinksType[]>(() => [
      {
        title: t('dcis.documents.links.sheets') as string,
        to: 'dcis-documents-documentId-sheets',
        icon: 'file-table-box-multiple-outline'
      },
      {
        title: t('dcis.documents.links.attributes') as string,
        to: 'dcis-documents-documentId-attributes',
        icon: 'page-next'
      },
      {
        title: t('dcis.documents.links.comments') as string,
        to: 'dcis-documents-documentId-comments',
        icon: 'comment-multiple'
      }
    ])

    const documentVersion = computed<string>(() =>
      t('dcis.grid.version', { version: activeDocument.value.version }) as string)

    const bc = computed<BreadCrumbsItem[]>(() => {
      const result: BreadCrumbsItem[] = [...props.breadCrumbs]
      if (activeDocument.value) {
        result.push({
          text: activeDocument.value.period.project.name,
          to: localePath({
            name: 'dcis-projects-projectId-periods',
            params: { projectId: activeDocument.value.period.project.id }
          }),
          exact: true
        }, {
          text: activeDocument.value.period.name,
          to: localePath({
            name: 'dcis-periods-periodId-documents',
            params: { periodId: toGlobalId('PeriodType', Number(activeDocument.value.period.id)) }
          }),
          exact: true
        }, {
          text: documentVersion.value,
          to: localePath({
            name: 'dcis-documents-documentId',
            params: { documentId: activeDocument.value.id }
          }),
          exact: true
        })
      }
      return result
    })

    const setFooter = inject<(state: boolean) => void>('setFooter')
    setFooter(false)
    onUnmounted(() => {
      setFooter(true)
    })

    return {
      activeDocument,
      loading,
      drawer,
      links,
      bc
    }
  }
})
</script>
