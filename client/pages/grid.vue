<template lang="pug">
  v-container
    v-card
      grid-toolbar(v-model="activeSheet" :document="document")
      v-card-text
        grid(:sheet="activeSheet")
</template>

<script lang="ts">
import { defineComponent, ref } from '#app'
import type { Ref } from '#app'
import type { UserType } from '~/types/graphql'
import type { DocumentType, SheetType } from '~/types/dcis'
import { useQueryRelay } from '~/composables'
import GridToolbar from '~/components/dcis/GridToolbar.vue'
import Grid from '~/components/dcis/Grid.vue'

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

    const getRandomUser = () => users.value[Math.floor(Math.random() * users.value.length)]

    const document: Ref<DocumentType> = ref<DocumentType>({
      id: '1',
      name: 'Тестовый документ',
      users: users.value.map((user: UserType) => ({
        id: user.id,
        user,
        active: getRandomBoolean(),
        color: getRandomColor()
      })),
      sheets: Array.from({ length: 5 }).map((_, sheetIndex) => {
        const columnsCount = (sheetIndex + 1) * 5
        const rowsCount = (sheetIndex + 2) * 5
        return {
          id: String(sheetIndex + 1),
          name: `Лист ${sheetIndex + 1}`,
          columnsCount,
          columnsDimension: Array.from({ length: columnsCount }).map((_, index) => index)
            .reduce((acc, columnIndex) => {
              return {
                ...acc,
                [columnIndex]: {
                  id: String(columnIndex),
                  index: columnIndex,
                  width: 75,
                  hidden: false,
                  collapsed: false
                }
              }
            }, {}),
          rowsCount,
          rowsDimension: Array.from({ length: rowsCount }).map((_, index) => index)
            .reduce((acc, rowIndex) => {
              return {
                ...acc,
                [rowIndex]: {
                  id: String(rowIndex),
                  index: rowIndex,
                  height: 35,
                  hidden: false,
                  collapsed: false
                }
              }
            }, {}),
          rows: Array.from({ length: rowsCount }).map((_, rowIndex) => ({
            cells: Array.from({ length: columnsCount }).map((_, cellIndex) => ({
              id: `${sheetIndex}${rowIndex}${cellIndex}`,
              kind: 'STRING',
              options: {
                align: 'LEFT',
                bold: false,
                italic: false
              },
              value: `${sheetIndex}${rowIndex}${cellIndex}`
            })),
            user: getRandomUser()
          })),
          mergeCells: {}
        }
      })
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
