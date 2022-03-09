<template lang="pug">
  v-dialog(v-model="drawer" width="600")
    template(#activator="{ on }")
      slot(:on="on")
    apollo-mutation(
      :mutation="require('~/gql/pages/mutations/page/change_page_avatar.graphql')"
      :variables="{ pageId: page.id, avatar }"
      @done="changePageAvatarDone"
      v-slot="{ mutate, loading, error }"
    )
      v-card
        v-card-title {{ $t('pages.page.changeAvatar.header') }}
          v-spacer
          v-btn(@click="close" icon)
            v-icon mdi-close
        v-card-subtitle {{ subtitle }}
        v-card-text
          v-alert(type="error" :value="!!error" dismissible) {{ error }}
          v-img.mb-4(v-if="avatar || page.avatar" :src="avatarSrc" height="450")
          v-file-input(
            v-model="avatar"
            :label="$t('pages.page.changeAvatar.avatar')"
            prepend-icon="mdi-camera"
            show-size
          )
        v-card-actions
          v-spacer
          v-btn(
            @click="mutate()"
            :disabled="!(avatar || page.avatar)"
            :loading="loading"
            color="primary"
          ) {{ buttonText }}
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import { PageType, ChangePageAvatarMutation } from '~/types/graphql'

@Component<ChangePageAvatar>({
  computed: {
    serverAvatarName () {
      return this.page.avatar ? this.page.avatar.match(/[^/]+$/)![0] : null
    },
    subtitle () {
      return this.page.avatar
        ? this.$t('pages.page.changeAvatar.serverAvatar', { name: this.serverAvatarName })
        : this.$t('pages.page.changeAvatar.noServerAvatar')
    },
    avatarSrc () {
      if (this.localAvatarSrc) {
        return this.localAvatarSrc
      }
      return `/${this.page.avatar}`
    },
    buttonText () {
      return this.avatar != null
        ? this.$t('pages.page.changeAvatar.change')
        : this.$t('pages.page.changeAvatar.delete')
    }
  },
  subscriptions () {
    const avatarWatch = this.$watchAsObservable('avatar')
    avatarWatch.subscribe(({ newValue }: { newValue: File | null }) => {
      this.setAvatarSrc(newValue)
    })
    return {
      avatarWatch
    }
  }
})
export default class ChangePageAvatar extends Vue {
  @Prop({ required: true, type: Object }) readonly page!: PageType

  drawer: boolean = false
  avatar: File | null = null
  localAvatarSrc: string | null = null
  serverAvatarName!: string | null
  subtitle!: string
  avatarSrc!: string | null | undefined
  buttonText!: string

  async setAvatarSrc (avatar: File | null) {
    if (avatar != null) {
      const fr = new FileReader()
      const result = new Promise<string>((resolve) => {
        fr.onload = () => resolve(fr.result as string)
      })
      fr.readAsDataURL(avatar)
      this.localAvatarSrc = await result
    } else {
      this.localAvatarSrc = null
    }
  }

  changePageAvatarDone ({ data: { changePageAvatar: { success } } }: { data: ChangePageAvatarMutation }) {
    if (success) {
      this.close()
    }
  }

  close () {
    this.drawer = false
    this.avatar = null
    this.$emit('close')
  }
}
</script>
