<template lang="pug">
viewer(:images="images" :options="options")
  template(#default="scope")
    div.row
      div.column(v-for="(chunk, i) in getChunks(scope.images)" :key="i")
        img(v-for="(image, j) in chunk" :src="image" :key="j")
</template>

<script lang="ts">
import type { PropType } from '#app'
import { defineComponent } from '#app'
import { component as Viewer } from 'v-viewer'
import 'viewerjs/dist/viewer.css'

export default defineComponent({
  components: { Viewer },
  props: {
    images: { type: Array as PropType<string[]>, required: true }
  },
  setup () {
    const options: Record<string, boolean> = {
      inline: false,
      button: true,
      navbar: true,
      title: false,
      toolbar: true,
      tooltip: false,
      movable: false,
      zoomable: false,
      rotatable: false,
      scalable: false,
      transition: true,
      fullscreen: false,
      keyboard: false
    }

    const getChunks = (arr: string[]) => {
      if (arr.length === 0) {
        return []
      }
      const perChunk = 3
      const newArray: string[][] = []
      for (let c = 0; c < perChunk; c++) {
        newArray.push([])
      }
      for (let i = 0; i < arr.length; i++) {
        const mod = i % perChunk
        newArray[mod].push(arr[i])
      }
      return newArray
    }
    return { options, getChunks }
  }
})
</script>

<style lang="sass">
.row
  display: flex
  flex-wrap: wrap
  padding: 0 4px

.column
  flex: 25%
  max-width: 25%
  padding: 0 4px

.column img
  margin-top: 8px
  vertical-align: middle
  width: 100%

</style>
