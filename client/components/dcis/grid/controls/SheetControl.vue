<template lang="pug">
v-menu(v-model="active" bottom close-on-content-click)
  template(#activator="{ on, attrs }")
    slot(:on="on" :attrs="attrs")
  v-list(dense)
    rename-dialog(
      v-slot="{ on, attrs }"
      @apply="renameSheet"
      :n="sheet.name"
      :label="String($t('dcis.grid.sheet.rename'))"
    )
      v-list-item(v-on="on" v-bind="attrs")
        v-list-item-icon  #[v-icon mdi-pencil]
        v-list-item-content
          v-list-item-title {{ $t('dcis.grid.sheet.rename') }}
</template>

<script lang="ts">
import { MutationUpdaterFn } from '@apollo/client'
import { defineComponent, PropType, ref } from '#app'
import { BaseSheetType } from '~/types/graphql'
import { useRenameSheetMutation } from '~/services/grapqhl/mutations/dcis/sheet_mutations'
import RenameDialog from '~/components/dcis/common/RenameDialog.vue'

export default defineComponent({
  components: { RenameDialog },
  props: {
    sheet: { type: Object as PropType<BaseSheetType>, required: true },
    update: { type: Function as PropType<MutationUpdaterFn<any>>, required: true }
  },
  setup (props) {
    const active = ref<boolean>(false)

    const renameSheet = async (n: string) => {
      await useRenameSheetMutation(props.sheet.id, n, props.update).mutate()
      active.value = false
    }

    return { active, renameSheet }
  }
})
</script>
