<template lang="pug">
  .d-flex.flex-column.align-center
    avatar-dialog(:item="user" size="200")
    v-btn(color="success" @click="selectAvatar").mt-3 {{ $t('ac.users.components.avatarView.changeAvatar') }}
</template>

<script lang="ts">
import type { Ref } from '#app'
import { defineComponent, toRef, useNuxtApp } from '#app'
import { useMutation } from '@vue/apollo-composable'
import { useSelectFiles } from '~/composables'
import { useAuthStore } from '~/store'
import {
  ChangeAvatarMutation, ChangeAvatarMutationPayload,
  ChangeAvatarMutationVariables, UserType
} from '~/types/graphql'
import changeAvatar from '~/gql/core/mutations/user/change_avatar.graphql'
import AvatarDialog from '~/components/users/AvatarDialog.vue'

export type ChangeAvatarMutationResult = { data: { changeAvatar: ChangeAvatarMutationPayload } }

export default defineComponent({
  components: { AvatarDialog },
  setup () {
    const userStore = useAuthStore()
    const { $store } = useNuxtApp()
    const user: Ref<UserType> = toRef(userStore, 'user')
    const { mutate: changeAvatarMutation, onDone } = useMutation<ChangeAvatarMutation, ChangeAvatarMutationVariables>(changeAvatar)

    onDone(({ data: { changeAvatar: { success, avatar } } }: ChangeAvatarMutationResult) => {
      if (success) {
        user.value.avatar = avatar
        // TODO: Убрать после полного перехода на pinia
        $store.dispatch('auth/changeUserAvatar', avatar)
      }
    })

    const { select: selectAvatar } = useSelectFiles((files: FileList) => {
      changeAvatarMutation({ userId: user.value.id, file: files[0] })
    }, { multiple: false })

    return { user, selectAvatar }
  }
})
</script>
