<template lang="pug">
  confirm-menu(
    @confirm="$emit('confirm')"
    @cancel="$emit('cancel')"
    :text="String($t('common.menu.deleteMenu.text', { itemName }))"
    yes-color="error"
    no-color="success"
  )
    template(#default="{ on }")
      slot(:on="on")
</template>

<script lang="ts">
import { defineComponent } from '#app'
import ConfirmMenu from '~/components/common/menu/ConfirmMenu.vue'

export default defineComponent({
  components: { ConfirmMenu },
  props: {
    itemName: {
      type: String,
      default () {
        return this.$t('common.menu.deleteMenu.defaultItemName')
      }
    }
  }
})
</script>
