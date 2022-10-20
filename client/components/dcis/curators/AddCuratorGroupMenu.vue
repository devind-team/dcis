<template lang="pug">
mutation-modal-form(
  :header="String($t('curators.addCuratorGroup.header'))"
  :button-text="String($t('curators.addCuratorGroup.buttonText'))"
  :mutation="addCuratorGroupMutation"
  :variables="variables"
  :update="(cache, result) => update(cache, result, 'curatorGroup', false)"
  mutation-name="addCuratorGroup"
  i18n-path="curators.addCuratorGroup"
  @close="close"
)
  template(#activator="{ on }")
    slot(name="activator" :on="on")
  template(#form)
    validation-provider(
      v-slot="{ errors, valid }"
      :name="String($t('curators.addCuratorGroup.name'))"
      rules="required|min:3"
    )
      v-text-field(
        v-model="name"
        :label="$t('curators.addCuratorGroup.name')"
        :error-messages="errors"
        :success="valid"
        autofocus
      )
    v-autocomplete(
      v-model="group"
      :label="$t('curators.addCuratorGroup.group')"
      :items="groups"
      :loading="groupsLoading"
      item-text="name"
      return-object
    )
</template>

<script lang="ts">
import { defineComponent, PropType, ref } from '#app'
import { useCommonQuery, AddUpdateType } from '~/composables'
import { GroupType, GroupsQuery, GroupsQueryVariables, AddCuratorGroupMutationVariables } from '~/types/graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'
import groupsQuery from '~/gql/core/queries/groups.graphql'
import addCuratorGroupMutation from '~/gql/dcis/mutations/curator/add_curator_group.graphql'

export default defineComponent({
  components: { MutationModalForm },
  props: {
    update: { type: Function as PropType<AddUpdateType>, required: true }
  },
  setup () {
    const name = ref<string>('')
    const group = ref<GroupType | null>(null)

    const variables = computed<AddCuratorGroupMutationVariables>(() => ({
      name: name.value,
      groupId: group.value ? group.value.id : null
    }))

    const { data: groups, loading: groupsLoading } = useCommonQuery<GroupsQuery, GroupsQueryVariables>({
      document: groupsQuery
    })

    const close = () => {
      name.value = ''
      group.value = null
    }

    return {
      addCuratorGroupMutation,
      name,
      group,
      groups,
      groupsLoading,
      variables,
      close
    }
  }
})
</script>
