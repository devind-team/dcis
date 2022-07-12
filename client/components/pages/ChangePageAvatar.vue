<template lang="pug">
mutation-modal-form(
  @done="changePageAvatarDone"
  :mutation="require('~/gql/pages/mutations/page/change_page_avatar.graphql')"
  :variables="{ pageId: page.id, avatar }"
  :header="$t('pages.page.changeAvatar.header')"
  :button-text="buttonText"
  mutation-name="changePageAvatar"
  i18n-path="pages.page.changeAvatar"
)
  template(#activator="{ on }")
    slot(:on="on")
  template(#form)
    v-img.mb-4(v-if="avatar || page.avatar" :src="avatarSrc" height="450")
    v-file-input(
      v-model="avatar"
      :label="$t('pages.page.changeAvatar.avatar')"
      prepend-icon="mdi-camera"
      show-size
      @change="setAvatarSrc"
    )
  template(#actions="{ invalid, loading, buttonText, setFormErrors, setError, setSuccess }")
    v-spacer
    v-btn(
      :disabled="invalid || !(avatar || page.avatar)"
      :loading="loading"
      type="submit"
      color="primary"
    ) {{ buttonText }}
</template>

<script lang="ts">
import { defineComponent, PropType, ref, computed } from '#app'
import { useI18n } from '~/composables'
import { PageType } from '~/types/graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'

export default defineComponent({
  components: { MutationModalForm },
  props: { page: { required: true, type: Object as PropType<PageType> } },
  setup (props, { emit }) {
    const { t } = useI18n()

    const avatar = ref<File | null>(null)
    const localAvatarSrc = ref<string | null>(null)

    const avatarSrc = computed(() => {
      if (localAvatarSrc.value) {
        return localAvatarSrc.value
      }
      return `/${props.page.avatar}`
    })

    const buttonText = computed(() => {
      return avatar.value
        ? t('pages.page.changeAvatar.change')
        : t('pages.page.changeAvatar.delete')
    })

    const setAvatarSrc = async () => {
      if (avatar.value) {
        const fr = new FileReader()
        const result = new Promise<string>((resolve) => {
          fr.onload = () => resolve(fr.result as string)
        })
        fr.readAsDataURL(avatar.value)
        localAvatarSrc.value = await result
      } else {
        localAvatarSrc.value = null
      }
    }

    const changePageAvatarDone = () => {
      avatar.value = null
      emit('close')
    }

    return { avatar, avatarSrc, setAvatarSrc, buttonText, changePageAvatarDone }
  }
})
</script>
