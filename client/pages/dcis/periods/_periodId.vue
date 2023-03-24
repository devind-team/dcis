<template lang="pug">
div
  left-navigator-driver(v-model="drawer" :items="links")
  v-progress-circular(v-if="loading" color="primary" indeterminate)
  nuxt-child(v-else :breadCrumbs="bc" :period="period" @update-drawer="drawer = !drawer")
</template>

<script lang="ts">
import type { PropType } from '#app'
import { computed, defineComponent, ref, provide } from '#app'
import { useRoute } from '#imports'
import { BreadCrumbsItem, LinksType } from '~/types/devind'
import { useI18n } from '~/composables'
import { usePeriodQuery } from '~/services/grapqhl/queries/dcis/periods'
import LeftNavigatorDriver from '~/components/common/grid/LeftNavigatorDriver.vue'

export default defineComponent({
  components: { LeftNavigatorDriver },
  middleware: 'auth',
  props: {
    breadCrumbs: { required: true, type: Array as PropType<BreadCrumbsItem[]> }
  },
  setup (props) {
    const { t, localePath } = useI18n()

    const route = useRoute()

    const {
      data: period,
      loading,
      update,
      changeUpdate
    } = usePeriodQuery(route.params.periodId)
    provide('periodUpdate', update)
    provide('periodChangeUpdate', changeUpdate)

    const drawer = ref<boolean>(false)
    const links = computed<LinksType[]>(() => {
      const result: LinksType[] = [
        {
          title: period.value && (period.value.isAdmin || period.value.isCurator)
            ? t('dcis.periods.links.monitoring') as string
            : t('dcis.periods.links.documents') as string,
          to: 'dcis-periods-periodId-documents',
          icon: 'file-table-box-multiple-outline'
        }
      ]
      if (!loading.value) {
        result.push({
          title: period.value.project.contentType.model === 'department'
            ? t('dcis.periods.links.departments') as string
            : t('dcis.periods.links.organizations') as string,
          to: 'dcis-periods-periodId-divisions',
          icon: 'briefcase-outline'
        })
      }
      result.push({
        title: t('dcis.periods.links.limitations') as string,
        to: 'dcis-periods-periodId-limitations',
        icon: 'shield-outline'
      })
      result.push({
        title: t('dcis.periods.links.aggregations') as string,
        to: 'dcis-periods-periodId-aggregations',
        icon: 'table-row'
      })
      if (!loading.value) {
        if (period.value.canChangeGroups) {
          result.push({
            title: t('dcis.periods.links.groups') as string,
            to: 'dcis-periods-periodId-groups',
            icon: 'account-group'
          })
        }
        if (period.value.canChangeUsers) {
          result.push({
            title: t('dcis.periods.links.users') as string,
            to: 'dcis-periods-periodId-users',
            icon: 'account-multiple'
          })
        }
        if (period.value.canChangeAttributes) {
          result.push({
            title: t('dcis.periods.links.attributes') as string,
            to: 'dcis-periods-periodId-attributes',
            icon: 'page-next'
          })
        }
        if (period.value.canChangeSheet) {
          result.push({
            title: t('dcis.periods.links.sheets') as string,
            to: 'dcis-periods-periodId-sheets',
            icon: 'table'
          })
        }
        if (period.value.canViewResult) {
          if (period.value.project.contentType.model === 'department') {
            result.push({
              title: t('dcis.periods.links.report') as string,
              to: 'dcis-periods-periodId-report',
              icon: 'table-multiple'
            })
          }
          if (period.value.project.contentType.model === 'organization') {
            result.push({
              title: t('dcis.periods.links.unload') as string,
              to: 'dcis-periods-periodId-unload',
              icon: 'microsoft-excel'
            })
          }
        }
        if (period.value.canChangeSettings || period.value.canDelete) {
          result.push({
            title: t('dcis.periods.links.settings') as string,
            to: 'dcis-periods-periodId-settings',
            icon: 'cogs'
          })
        }
      }
      return result
    })

    const bc = computed<BreadCrumbsItem[]>(() => {
      if (loading.value) {
        return props.breadCrumbs
      }
      return [
        ...props.breadCrumbs,
        {
          text: period.value.project.name,
          to: localePath({
            name: 'dcis-projects-projectId-periods',
            params: { projectId: period.value.project.id }
          }),
          exact: true
        },
        { text: period.value.name, to: localePath({ name: 'dcis-periods-periodId-documents' }), exact: true }
      ]
    })

    return { route, period, loading, drawer, links, bc }
  }
})
</script>
