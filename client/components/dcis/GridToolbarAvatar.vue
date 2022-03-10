<template lang="pug">
  v-tooltip(bottom)
    template(#activator="{ on }")
      v-avatar(
        v-on="on"
        :color="documentUser.active ? documentUser.color : '#BDBDBD'"
        :style="`border: 5px solid ${documentUser.active ? documentUser.color : '#BDBDBD'}`"
        size="53"
      ).mr-2
        v-img(v-if="!!documentUser.user.avatar" :src="`/${documentUser.user.avatar}`")
        .headline(v-else) {{ documentUser.user.lastName[0] }}{{ documentUser.user.firstName[0] }}
    .d-flex.flex-column.align-center
      span {{ $getUserFullName(documentUser.user) }}
      span {{ documentUser.active ? t('grid.toolbarAvatar.active') : t('grid.toolbarAvatar.notActive') }}
</template>

<script lang="ts">
import { defineComponent } from '#app'
import type { PropType } from '#app'
import { useI18n } from '~/composables'
import type { DocumentUserType } from '~/types/dcis'

export default defineComponent({
  props: {
    documentUser: {
      type: Object as PropType<DocumentUserType>,
      required: true
    }
  },
  setup () {
    const { t } = useI18n()
    return { t }
  }
})
</script>
