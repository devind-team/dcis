<template lang="pug">
  v-row
    v-col(cols="12" md="3")
      slot(name="links")
        v-card
          v-list
            template(v-for="link in links")
              v-list-item(
                v-if="link.permissions === undefined || link.permissions && hasPerm(link.permissions)"
                :key="link.to"
                :to="localePath({ name: link.to, params: link.params })"
              )
                v-list-item-avatar
                  v-icon(left) mdi-{{ link.icon }}
                v-list-item-content {{ link.title }}
    v-col(cols="12" md="9")
      slot
</template>

<script lang="ts">
import type { PropType } from '#app'
import { defineComponent } from '#app'
import { LinksType } from '~/types/devind'
import { useAuthStore } from '~/store'

export default defineComponent({
  props: {
    links: { type: Array as PropType<LinksType[]>, required: true }
  },
  setup () {
    const { hasPerm } = useAuthStore()
    return { hasPerm }
  }
})
</script>
