<template lang="pug">
  .d-flex.flex-column.align-center
    avatar-dialog(:item="user" size="200")
    v-btn(color="success" @click="selectAvatar").mt-3 {{ $t('ac.users.components.avatarView.changeAvatar') }}
</template>

<script lang="ts">
import { useMutation } from '@vue/apollo-composable'
import type { Ref } from '#app'
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
    const authStore = useAuthStore()
    const user: Ref<UserType> = toRef(authStore, 'user')
    const { mutate: changeAvatarMutation, onDone } = useMutation<ChangeAvatarMutation, ChangeAvatarMutationVariables>(changeAvatar)

    onDone(({ data: { changeAvatar: { errors, avatar } } }: ChangeAvatarMutationResult) => {
      if (!errors.length) {
        user.value.avatar = avatar
      }
    })

    const { select: selectAvatar } = useSelectFiles((files: FileList) => {
      changeAvatarMutation({ userId: user.value.id, file: files[0] })
    }, { multiple: false })

    return { user, selectAvatar }
  }
})
</script>
