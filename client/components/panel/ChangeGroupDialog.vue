<template lang="pug">
  mutation-modal-form(
    :header="String($t('panel.ac.users.changeGroups.header'))"
    :button-text="String($t('panel.ac.users.changeGroups.buttonText'))"
    :mutation="require('~/gql/core/mutations/user/change_user_groups.graphql')"
    :variables="{ userId: user.id, groupsId: selectedGroupsId }"
    :update="(...args) => $emit('update', args)"
    mutation-name="changeUserGroups"
    errors-in-alert
    @close="selectedGroups = user.groups"
  )
    template(#activator="{ on }")
      slot(:on="on")
    template(#form)
      v-list
        v-list-item-group(v-model="selectedGroupsId" multiple color="primary")
          v-list-item(v-for="group in groups" :key="group.id" :value="group.id") {{ group.name }}
</template>

<script lang="ts">
import type { PropType, Ref, WritableComputedRef } from '#app'
import { computed, defineComponent, ref } from '#app'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'
import { GroupType, UserType } from '~/types/graphql'

export default defineComponent({
  components: { MutationModalForm },
  props: {
    user: { type: Object as PropType<UserType>, required: true },
    groups: { type: Array as PropType<GroupType[]>, required: true }
  },
  setup (props) {
    const selectedGroups: Ref<GroupType[]> = ref<GroupType[]>(props.user.groups)
    const selectedGroupsId: WritableComputedRef<string[]> = computed<string[]>({
      get (): string[] {
        return selectedGroups.value.map((group: GroupType) => group.id)
      },
      set (value: string[]): void {
        selectedGroups.value = props.groups.filter((group: GroupType) => value.includes(group.id))
      }
    })
    return { selectedGroups, selectedGroupsId }
  }
})
</script>
