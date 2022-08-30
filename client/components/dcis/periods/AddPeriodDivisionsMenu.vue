<template lang="pug">
v-menu(v-model="active" transition="slide-y-transition" offset-y left)
  template(#activator="{ on }")
    slot(name="activator" :on="on")
  v-list(dense)
    add-period-divisions(
      @close="close"
      :header="addHeader"
      :button-text="addButtonText"
      :period="period"
      :update="addDivisionsUpdate"
    )
      template(#activator="{ on }")
        v-list-item(v-on="on")
          v-list-item-icon
            v-icon mdi-format-list-checks
          v-list-item-content {{ addButtonText }} из списка
    add-period-divisions-from-file(
      @close="close"
      :header="addHeader"
      :button-text="addButtonText"
      :period="period"
      :update="addDivisionsFromFileUpdate"
    )
      template(#activator="{ on }")
        v-list-item(v-on="on")
          v-list-item-icon
            v-icon mdi-file
          v-list-item-content {{ addButtonText }} из файла
</template>

<script lang="ts">
import { defineComponent, PropType, ref } from '#app'
import { DataProxy } from 'apollo-cache'
import AddPeriodDivisions, { AddDivisionsMutationResult } from '~/components/dcis/periods/AddPeriodDivisions.vue'
import { PeriodType } from '~/types/graphql'
import AddPeriodDivisionsFromFile, {
  AddDivisionsFromFileMutationResult
} from '~/components/dcis/periods/AddPeriodDivisionsFromFile.vue'

export default defineComponent({
  components: { AddPeriodDivisionsFromFile, AddPeriodDivisions },
  props: {
    addHeader: { type: String, required: true },
    addButtonText: { type: String, required: true },
    period: { type: Object as PropType<PeriodType> },
    addDivisionsUpdate: {
      type: Function as PropType<(cache: DataProxy, result: AddDivisionsMutationResult) => void>,
      required: true
    },
    addDivisionsFromFileUpdate: {
      type: Function as PropType<(cache: DataProxy, result: AddDivisionsFromFileMutationResult) => void>,
      required: true
    }
  },
  setup () {
    const active = ref<boolean>(false)

    const close = () => {
      active.value = false
    }

    return { active, close }
  }
})
</script>
