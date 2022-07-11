<template functional lang="pug">
div(class="prose prose-sm sm:prose-sm lg:prose xl:prose-lg focus:outline-none")
  slot
    component(:is="$options.components.VSheet" v-html="props.html")
</template>

<script lang="ts">
import { defineComponent } from '#app'
import { VSheet } from 'vuetify/lib/components'

export default defineComponent({
  components: { VSheet },
  props: {
    html: { type: String, default: '' }
  }
})
</script>
