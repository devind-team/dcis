<template lang="pug">
left-navigator-container(:bread-crumbs="bc" fluid @update-drawer="$emit('update-drawer')")
  template(#header) {{ $t('curators.name') }}
    v-spacer
    add-curator-group-menu(v-if="hasPerm('dcis.add_curatorgroup')" :update="addUpdate")
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
      change-curator-group-users(v-if="hasPerm('dcis.change_curatorgroup')" :curator-group="item")
        template(#activator="{ on: onMenu }")
          v-tooltip(bottom)
            template(#activator="{ on: onTooltip, attrs }")
              v-btn.mr-1(v-on="{ ...onMenu, ...onTooltip }" v-bind="attrs" color="primary" icon)
                v-icon mdi-account-edit
            span {{ $t('curators.tooltips.changeUsers') }}
      v-tooltip(v-if="hasPerm('dcis.change_curatorgroup')" bottom)
        template(#activator="{ on, attrs }")
          v-btn.mx-1(v-on="on" v-bind="attrs" icon color="primary")
            v-icon mdi-briefcase-edit-outline
        span {{ $t('curators.tooltips.changeOrganizations') }}
      delete-menu(
        v-if="hasPerm('dcis.delete_curatorgroup')"
        :item-name="String($t('curators.deleteCuratorGroup.itemName'))"
        @confirm="deleteCuratorGroup({ id: item.id })"
      )
        template(#default="{ on: onMenu }")
          v-tooltip(bottom)
            template(#activator="{ on: onTooltip, attrs }")
              v-btn.ml-1(v-on="{ ...onMenu, ...onTooltip }" v-bind="attrs" icon color="error")
                v-icon mdi-delete
            span {{ $t('curators.tooltips.delete') }}
</template>

<script lang="ts">
import { DataTableHeader } from 'vuetify'
import { useMutation } from '@vue/apollo-composable'
import { computed, defineComponent, PropType } from '#app'
import { useAuthStore } from '~/stores'
import {
  CuratorGroupsQuery,
  CuratorGroupsQueryVariables,
  DeleteCuratorGroupMutation,
  DeleteCuratorGroupMutationVariables
} from '~/types/graphql'
import { BreadCrumbsItem } from '~/types/devind'
import { useI18n, useCommonQuery } from '~/composables'
import curatorGroupsQuery from '~/gql/dcis/queries/curator_groups.graphql'
import deleteCuratorGroupMutation from '~/gql/dcis/mutations/curator/delete_curator_group.graphql'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import AddCuratorGroupMenu from '~/components/dcis/curators/AddCuratorGroupMenu.vue'
import ChangeCuratorGroupUsers from '~/components/dcis/curators/ChangeCuratorGroupUsers.vue'
import DeleteMenu from '~/components/common/menu/DeleteMenu.vue'

export default defineComponent({
  components: {
    LeftNavigatorContainer,
    AddCuratorGroupMenu,
    ChangeCuratorGroupUsers,
    DeleteMenu
  },
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true }
  },
  setup (props) {
    const { t, localePath } = useI18n()

    const { hasPerm } = useAuthStore()

    const bc = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      { text: t('curators.name') as string, to: localePath({ name: 'panel-ac-curator_groups' }), exact: true }
    ]))

    const headers = computed<DataTableHeader[]>(() => {
      const result: DataTableHeader[] = [
        { text: t('curators.tableHeaders.name') as string, value: 'name' },
        { text: t('curators.tableHeaders.group') as string, value: 'group' }
      ]
      if (hasPerm(['dcis.change_curatorgroup', 'dcis.delete_curatorgroup'], true)) {
        result.push({
          text: t('curators.tableHeaders.actions') as string,
          value: 'actions',
          align: 'center',
          sortable: false
        })
      }
      return result
    })

    const { data: curatorGroups, addUpdate, deleteUpdate } = useCommonQuery<CuratorGroupsQuery, CuratorGroupsQueryVariables>({
      document: curatorGroupsQuery
    })

    /**
     * Удаление группы
     */
    const { mutate: deleteCuratorGroup } = useMutation<
      DeleteCuratorGroupMutation,
      DeleteCuratorGroupMutationVariables
    >(deleteCuratorGroupMutation, {
      update: deleteUpdate
    })

    return {
      hasPerm,
      bc,
      headers,
      curatorGroups,
      addUpdate,
      deleteCuratorGroup
    }
  }
})
</script>
