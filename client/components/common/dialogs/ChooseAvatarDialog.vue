<template lang="pug">
v-dialog(v-model="active" width="600")
  template(#activator="{ on }")
    slot(:on="on")
  v-card
    v-card-title {{ $t('common.dialogs.chooseAvatarDialog.chooseAvatar') }}
      v-spacer
      v-btn(icon @click="active=false")
        v-icon mdi-close
    v-card-text
      v-file-input(
        v-model="avatar"
        :label="$t('common.dialogs.chooseAvatarDialog.avatar')"
        prepend-icon="mdi-camera"
        show-size
      )
    v-card-actions
      v-spacer
      v-btn(color="primary" @click="changeAvatar") {{ text }}
</template>

<script lang="ts">
import type { ComputedRef, Ref, SetupContext } from '#app'
import { computed, defineComponent, ref } from '#app'
import { useI18n } from '~/composables'

export default defineComponent({
  setup (_, { emit }: SetupContext) {
    const { t } = useI18n()
    const active: Ref<boolean> = ref<boolean>(false)
    const avatar: Ref<File | null> = ref<File | null>(null)
    const text: ComputedRef<string> = computed<string>(
      () => t(`common.dialogs.chooseAvatarDialog.${avatar.value ? 'choose' : 'delete'}`) as string
    )

    const changeAvatar = () => {
      active.value = false
      emit('input', avatar.value)
    }
    const close = () => {
      active.value = false
      avatar.value = null
      emit('input')
    }
    return { active, avatar, text, changeAvatar, close }
  }
})
</script>
