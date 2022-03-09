<template lang="pug">
  v-container
    v-card
      grid-toolbar(v-model="activeSheet" :document="document")
      v-card-text
        grid
</template>

<script lang="ts">
import { defineComponent, ref } from '#app'
import type { Ref } from '#app'
import type { UserType } from '~/types/graphql'
import type { DocumentType, SheetType } from '~/types/grid'
import { useQueryRelay } from '~/composables'
import GridToolbar from '~/components/grid/GridToolbar.vue'
import Grid from '~/components/grid/Grid.vue'

const colors = [
  '#F44336', '#E91E63', '#9C27B0', '#673AB7',
  '#3F51B5', '#2196F3', '#03A9F4', '#00BCD4',
  '#009688', '#4CAF50', '#8BC34A', '#CDDC39',
  '#FFEB3B', '#FFC107', '#FF9800', '#FF5722',
  '#795548', '#607D8B'
]
const getRandomColor = () => colors[Math.floor(Math.random() * colors.length)]
const getRandomBoolean = () => !Math.round(Math.random())

export default defineComponent({
  components: {
    GridToolbar,
    Grid
  },
  setup () {
    const { data: users } = useQueryRelay<UserType>({
      document: require('~/gql/core/queries/users')
    })

    const document: Ref<DocumentType> = ref<DocumentType>({
      id: '1',
      name: 'Тестовый документ',
      users: users.value.map((user: UserType) => ({
        id: user.id,
        user,
        active: getRandomBoolean(),
        color: getRandomColor()
      })),
      sheets: Array.from({ length: 5 }).map((_, index) => ({
        id: String(index + 1),
        name: `Лист ${index + 1}`
      }))
    })
    const activeSheet: Ref<SheetType> = ref<SheetType>(document.value.sheets[0])

    return {
      users,
      activeSheet,
      document
    }
  }
})
</script>
