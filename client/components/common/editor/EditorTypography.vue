<template functional lang="pug">
  div(class="prose prose-sm sm:prose-sm lg:prose xl:prose-lg focus:outline-none")
    slot
      component(:is="$options.components.VSheet" v-html="props.html")
</template>

<script lang="ts">
import Vue from 'vue'
import { VSheet } from 'vuetify/lib/components'

export default Vue.extend<any, any, any, any>({
  components: { VSheet },
  props: {
    html: { type: String, default: '' }
  }
})
</script>
