<template lang="pug">
mutation-modal-form(
  :header="String($t('curators.changeCuratorGroupOrganizations.header'))"
  :subheader="curatorGroup.name"
  :button-text="String($t('curators.changeCuratorGroupOrganizations.buttonText'))"
  :mutation="addOrganizationsCuratorGroupMutation"
  :variables="addVariables"
  :update="addOrganizationsUpdate"
  :success-close="false"
  :success-message="String($t('curators.changeCuratorGroupOrganizations.successMessage'))"
  mutation-name="addOrganizationsCuratorGroup"
  i18n-path="curators.changeCuratorGroupOrganizations"
  width="1500"
  @first-activated="firstActivated"
  @close="close"
  @done="addOrganizationsDone"
)
  template(#activator="{ on }")
    slot(name="activator" :on="on")
  template(#form)
    v-data-table(
      :headers="headers"
      :items="groupOrganizations"
      :loading="curatorGroupLoading"
      disable-pagination
      hide-default-footer
    )
      template(#item.name="{ item }") {{ item.name }}
      template(#item.actions="{ item }")
        delete-menu(
          :item-name="String($t('curators.changeCuratorGroupOrganizations.deleteItemName'))"
          @confirm="deleteOrganization({ curatorGroupId: curatorGroup.id, organizationId: item.id })"
        )
          template(#default="{ on: onMenu }")
            v-tooltip(bottom)
              template(#activator="{ on: onTooltip, attrs }")
                v-btn.ml-1(v-on="{ ...onMenu, ...onTooltip }" v-bind="attrs" color="error" icon)
                  v-icon mdi-delete
              span {{ $t('curators.changeCuratorGroupOrganizations.deleteTooltip') }}
    validation-provider(
      ref="newOrganizationsValidationProvider"
      v-slot="{ errors, valid }"
      :name="String($t('curators.changeCuratorGroupOrganizations.newOrganizations'))"
      rules="required"
    )
      v-autocomplete.mt-2(
        v-model="newOrganizations"
        :label="$t('curators.changeCuratorGroupOrganizations.newOrganizations')"
        :items="organizations"
        :loading="organizationsLoading"
        :search-input.sync="organizationsSearch"
        :error-messages="errors"
        :success="valid"
        item-value="id"
        multiple
        chips
        deletable-chips
        return-object
        no-filter
      )
          template(#selection="{ item }")
            v-chip(close @click:close="userChipClose(item)") {{ item.name }}
          template(#item="{ item }")
            v-list-item-content
              v-list-item-title {{ item.name }}
</template>

<script lang="ts">
import { computed, defineComponent, PropType, ref } from '#app'
import { DataProxy } from '@apollo/client'
import { VariablesParameter } from '@vue/apollo-composable/dist/useQuery'
import { useMutation } from '@vue/apollo-composable'
import { DataTableHeader } from 'vuetify'
import { ValidationProvider } from 'vee-validate'
import {
  OrganizationType,
  OrganizationFieldFragment,
  CuratorGroupType,
  CuratorGroupOrganizationsQuery,
  CuratorGroupOrganizationsQueryVariables,
  CuratorGroupNewOrganizationsQuery,
  CuratorGroupNewOrganizationsQueryVariables,
  AddOrganizationsCuratorGroupMutationVariables,
  AddOrganizationsCuratorGroupPayload,
  DeleteOrganizationCuratorGroupMutation,
  DeleteOrganizationCuratorGroupMutationVariables
} from '~/types/graphql'
import { useCommonQuery, useDebounceSearch, useI18n, useQueryRelay } from '~/composables'
import curatorGroupOrganizationsQuery from '~/gql/dcis/queries/curator_group_organizations.graphql'
import curatorGroupNewOrganizationsQuery from '~/gql/dcis/queries/curator_group_new_organizations.graphql'
import addOrganizationsCuratorGroupMutation from '~/gql/dcis/mutations/curator/add_organizations_curator_group.graphql'
import deleteOrganizationCuratorGroupMutation from '~/gql/dcis/mutations/curator/delete_organization_curator_group.graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'
import DeleteMenu from '~/components/common/menu/DeleteMenu.vue'

type AddOrganizationsCuratorGroupResult = { data: { addOrganizationsCuratorGroup: AddOrganizationsCuratorGroupPayload }}

export default defineComponent({
  components: { MutationModalForm, DeleteMenu },
  props: {
    curatorGroup: { type: Object as PropType<CuratorGroupType>, required: true }
  },
  setup (props) {
    const { t } = useI18n()

    const newOrganizationsValidationProvider = ref<InstanceType<typeof ValidationProvider | null>>(null)

    const firstActivated = () => {
      options.value.enabled = true
    }

    const headers = computed<DataTableHeader[]>(() => [
      { text: t('curators.changeCuratorGroupOrganizations.tableHeaders.name') as string, value: 'name' },
      {
        text: t('curators.changeCuratorGroupOrganizations.tableHeaders.actions') as string,
        value: 'actions',
        align: 'center',
        sortable: false
      }
    ])

    const options = ref<{ enabled: boolean }>({ enabled: false })

    const { data: curatorGroup, loading: curatorGroupLoading, update: curatorGroupUpdate } = useCommonQuery<
      CuratorGroupOrganizationsQuery,
      CuratorGroupOrganizationsQueryVariables
    >({
      document: curatorGroupOrganizationsQuery,
      options,
      variables: () => ({ curatorGroupId: props.curatorGroup.id })
    })
    const groupOrganizations = computed<OrganizationFieldFragment[]>(
      () => curatorGroup.value ? curatorGroup.value.organization : [])

    const { mutate: deleteOrganizationMutate } = useMutation<
      DeleteOrganizationCuratorGroupMutation,
      DeleteOrganizationCuratorGroupMutationVariables
    >(deleteOrganizationCuratorGroupMutation, {
      update: (cache, result) => curatorGroupUpdate(
        cache,
        result,
        (
          dataCache,
          { data: { deleteOrganizationCuratorGroup: { success, id } } }
        ) => {
          if (success) {
            dataCache.curatorGroup.organization = dataCache.curatorGroup.organization.filter(
              (organization: OrganizationFieldFragment) => organization.id !== id
            )
          }
          return dataCache
        }
      )
    })
    const deleteOrganization = async (variables: DeleteOrganizationCuratorGroupMutationVariables) => {
      await deleteOrganizationMutate(variables)
      await refetchOrganizations()
    }

    const { search: organizationsSearch, debounceSearch: organizationsDebounceSearch } = useDebounceSearch()
    const { data: organizations, loading: organizationsLoading, refetch: refetchOrganizations } = useQueryRelay<
      CuratorGroupNewOrganizationsQuery,
      CuratorGroupNewOrganizationsQueryVariables,
      OrganizationType
      >({
        document: curatorGroupNewOrganizationsQuery,
        options,
        variables: () => {
          const result: VariablesParameter<CuratorGroupNewOrganizationsQueryVariables> = {
            search: organizationsDebounceSearch.value
          }
          if (organizationsDebounceSearch.value) {
            result.first = undefined
          }
          return result
        }
      })
    const newOrganizations = ref<OrganizationType[]>([])
    const organizationChipClose = (organization: OrganizationType) => {
      newOrganizations.value = newOrganizations.value.filter(
        (existOrganization: OrganizationType) => existOrganization.id !== organization.id)
    }
    const addVariables = computed<AddOrganizationsCuratorGroupMutationVariables>(() => ({
      curatorGroupId: props.curatorGroup.id,
      organizationIds: newOrganizations.value.map((organization: OrganizationType) => organization.id)
    }))
    const addOrganizationsUpdate = (cache: DataProxy, result: AddOrganizationsCuratorGroupResult) => {
      curatorGroupUpdate(
        cache,
        result,
        (dataCache, { data: { addOrganizationsCuratorGroup: { success, organizations } } }) => {
          if (success) {
            dataCache.curatorGroup.organization = [
              ...dataCache.curatorGroup.organization,
              ...(organizations as OrganizationFieldFragment[])
            ]
            dataCache.curatorGroup.organization.sort((
              org1: OrganizationFieldFragment, org2: OrganizationFieldFragment) => {
              return Number(new Date(org1.createdAt)) - Number(new Date(org2.createdAt))
            })
          }
          return dataCache
        }
      )
    }

    const addOrganizationsDone = () => {
      newOrganizations.value = []
      newOrganizationsValidationProvider.value.reset()
      refetchOrganizations()
    }

    const close = () => {
      newOrganizations.value = []
    }

    return {
      firstActivated,
      addOrganizationsCuratorGroupMutation,
      newOrganizationsValidationProvider,
      headers,
      groupOrganizations,
      curatorGroupLoading,
      curatorGroupUpdate,
      deleteOrganizationMutate,
      deleteOrganization,
      organizations,
      organizationsSearch,
      organizationsLoading,
      refetchOrganizations,
      newOrganizations,
      organizationChipClose,
      addVariables,
      addOrganizationsUpdate,
      addOrganizationsDone,
      close
    }
  }
})
</script>

<style scoped>

</style>
