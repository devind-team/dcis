<template lang="pug">
v-avatar(v-bind="$attrs" color="primary" :size="size")
  v-dialog(v-model="active" v-if="!!item.avatar && showDialog" width="520")
    template(#activator="{ on }")
      v-img(v-on="on" :src="`/${item.avatar}`")
    v-card
      v-card-title {{ $t('ac.users.components.avatarDialog.UserAvatar') }} {{ item.lastName }} {{ item.firstName }}
        v-spacer
        v-btn(@click="active = false" icon)
          v-icon mdi-close
      v-card-subtitle {{ item.username }} #[a(:href="`mailto: ${item.email}`") {{ item.email }}]
      v-card-text
        v-img(:src="`/${item.avatar}`" width="600")
  v-img(v-else-if="!!item.avatar" :src="`/${item.avatar}`")
  .headline(v-else style="color: black") {{ item.lastName[0] }}{{ item.firstName[0] }}
</template>

<script lang="ts">
import type { PropType, Ref } from '#app'
import { defineComponent, ref } from '#app'
import { UserType } from '~/types/graphql'

export default defineComponent({
  props: {
    item: { type: Object as PropType<UserType>, required: true },
    showDialog: { type: Boolean, default: true },
    size: { type: [String, Number], default: 46 }
  },
  setup () {
    const active: Ref<boolean> = ref<boolean>(false)
    return { active }
  }
})
</script>
