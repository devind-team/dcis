<template lang="pug">
  v-data-iterator(:items="items" disable-pagination hide-default-footer)
    template(#default="{ items }")
      v-row(align="stretch")
        template(v-for="card in items")
          v-col(
            v-if="!card.permissions || card.permissions && hasPerm(card.permissions, card.permOr || false)"
            :key="card.icon"
            cols="12"
            sm="6"
            md="4"
            lg="4"
          )
            v-card(:to="card.to" height="100%" ripple outlined)
              v-card-text.text-center
                v-icon(size="120" :color="card.color") {{ card.icon }}
                .body-1.text-center {{ card.title }}
</template>

<script lang="ts">
import type { PropType } from '#app'
import { defineComponent } from '#app'
import { LinksType } from '~/types/devind'
import { useAuthStore } from '~/stores'

export default defineComponent({
  props: {
    items: { type: Array as PropType<LinksType[]>, required: true }
  },
  setup () {
    const { hasPerm } = useAuthStore()
    return { hasPerm }
  }
})
</script>
