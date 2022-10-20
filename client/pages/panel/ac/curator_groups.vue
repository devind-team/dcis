<template lang="pug">
left-navigator-container(:bread-crumbs="bc" fluid @update-drawer="$emit('update-drawer')")
  template(#header) {{ $t('curators.name') }}
    v-spacer
    add-curator-group-menu(:update="addUpdate")
      template(#activator="{ on }")
        v-btn(v-on="on" color="primary") {{ $t('curators.addCuratorGroup.buttonText') }}
  template(#subheader)
    template(v-if="curatorGroups")
      | {{ $t('shownOf', { count: curatorGroups.length, totalCount: curatorGroups.length }) }}
  v-data-table(:headers="headers" :items="curatorGroups" disable-pagination hide-default-footer)
    template(#item.group="{ item }")
      template(v-if="item.group") {{ item.group.name }}
      strong(v-else) &ndash;
    template(#item.actions="{ item }")
      v-tooltip(bottom)
        template(#activator="{ on, attrs }")
          v-btn.mr-1(v-on="on" v-bind="attrs" icon color="primary")
            v-icon mdi-account-edit
        span {{ $t('curators.tooltips.changeUsers') }}
      v-tooltip(bottom)
        template(#activator="{ on, attrs }")
          v-btn.mx-1(v-on="on" v-bind="attrs" icon color="primary")
            v-icon mdi-briefcase-edit-outline
        span {{ $t('curators.tooltips.changeOrganizations') }}
      v-tooltip(bottom)
        template(#activator="{ on, attrs }")
          v-btn.ml-1(v-on="on" v-bind="attrs" icon color="error")
            v-icon mdi-delete
        span {{ $t('curators.tooltips.delete') }}
</template>

<script lang="ts">
import { DataTableHeader } from 'vuetify'
import { computed, defineComponent, PropType } from '#app'
import { CuratorGroupsQuery, CuratorGroupsQueryVariables } from '~/types/graphql'
import { BreadCrumbsItem } from '~/types/devind'
import { useI18n, useCommonQuery } from '~/composables'
import curatorGroupsQuery from '~/gql/dcis/queries/curator_groups.graphql'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import AddCuratorGroupMenu from '~/components/dcis/curators/AddCuratorGroupMenu.vue'

export default defineComponent({
  components: {
    LeftNavigatorContainer,
    AddCuratorGroupMenu
  },
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true }
  },
  setup (props) {
    const { t, localePath } = useI18n()

    const bc = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      { text: t('curators.name') as string, to: localePath({ name: 'panel-ac-curator_groups' }), exact: true }
    ]))

    const headers: DataTableHeader[] = [
      { text: t('curators.tableHeaders.name') as string, value: 'name' },
      { text: t('curators.tableHeaders.group') as string, value: 'group' },
      { text: t('curators.tableHeaders.actions') as string, value: 'actions', align: 'center', sortable: false }
    ]

    const { data: curatorGroups, addUpdate } = useCommonQuery<CuratorGroupsQuery, CuratorGroupsQueryVariables>({
      document: curatorGroupsQuery
    })

    return {
      bc,
      headers,
      curatorGroups,
      addUpdate
    }
  }
})
</script>
