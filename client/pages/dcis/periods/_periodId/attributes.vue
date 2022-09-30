<template lang="pug">
left-navigator-container(:bread-crumbs="bc" @update-drawer="$emit('update-drawer')")
  template(#header) {{ $t('dcis.periods.links.attributes') }}
    v-spacer
    add-attribute-menu(v-slot="{ on, attrs}")
      v-btn(v-on="on" v-bind="attrs" color="primary") {{ $t('dcis.attributes.adds') }}
  template(v-if="!loading")
    v-row(v-for="attribute in attributes" :key="attribute.id")
      v-col(cols="12" md="3") {{ attribute.name }}
        .caption {{ attribute.placeholder }}
        v-tooltip(bottom)
          template(#activator="{ on, attrs}")
            v-btn(v-on="on" v-bind="attrs" icon)
              v-icon mdi-plus
          span {{ $t('dcis.attributes.add') }}
        v-tooltip(bottom)
          template(#activator="{ on, attrs }")
            v-btn(v-on="on" v-bind="attrs" icon)
              v-icon mdi-delete
          span {{ $t('dcis.attributes.delete') }}
      v-col(cols="12" md="9")
        v-data-table(
          :headers="headers"
          :items="attribute.children"
          disable-pagination
          disable-filtering
          hide-default-footer
        )
          template(#item.action="{ item }")
            v-menu(bottom)
              template(#activator="{ on, attrs}")
                v-btn(v-on="on" v-bind="attrs" icon)
                  v-icon mdi-dots-vertical
              v-list
                v-list-item {{ $t('dcis.attributes.change') }}
                v-list-item {{ $t('dcis.attributes.delete') }}
  v-progress-circular(v-else color="primary" indeterminate)
</template>

<script lang="ts">
import type { ComputedRef, PropType } from '#app'
import { computed, defineComponent, useNuxt2Meta } from '#app'
import { DataTableHeader } from 'vuetify'
import { useCommonQuery, useI18n } from '~/composables'
import { BreadCrumbsItem } from '~/types/devind'
import { AttributesQuery, AttributesQueryVariables, PeriodType } from '~/types/graphql'
import attributesQuery from '~/gql/dcis/queries/attributes.graphql'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import AddAttributeMenu from '~/components/dcis/attributes/AddAttributeMenu.vue'

export default defineComponent({
  components: { AddAttributeMenu, LeftNavigatorContainer },
  middleware: 'auth',
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true }
  },
  setup (props) {
    const { t, localePath } = useI18n()
    useNuxt2Meta({ title: props.period.name })

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      {
        text: t('dcis.periods.links.attributes') as string,
        to: localePath({ name: 'dcis-periods-periodId-attributes' }),
        exact: true
      }
    ]))

    const headers: ComputedRef<DataTableHeader[]> = computed<DataTableHeader[]>(() => ([
      { text: t('dcis.attributes.tableHeaders.name') as string, value: 'name', width: '45%' },
      { text: t('dcis.attributes.tableHeaders.key') as string, value: 'key', width: '10%' },
      { text: t('dcis.attributes.tableHeaders.value') as string, value: 'value', width: '35%' },
      { text: t('dcis.attributes.tableHeaders.action') as string, value: 'action', width: '10%' }
    ]))

    const { data: attributes, loading } = useCommonQuery<AttributesQuery, AttributesQueryVariables, 'attributes'>({
      document: attributesQuery,
      variables: () => ({
        periodId: props.period.id
      })
    })

    return { bc, headers, attributes, loading }
  }
})
</script>
