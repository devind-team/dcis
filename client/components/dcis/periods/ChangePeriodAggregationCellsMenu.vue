<template lang="pug">
v-menu(v-model="active", transition="slide-y-transition" offset-y left)
  template(#activator="{ on, attrs }")
    slot(name="activator" :on="on" :attrs="attrs")
  v-list(dense)
    update-period-aggregation-cells-from-file(:period="period", :update="fromFileUpdate")
      template(#activator="{ on, attrs }")
        v-list-item(v-on="on" v-bind="attrs")
          v-list-item-icon
            v-icon mdi-file
          v-list-item-content {{ $t('dcis.periods.aggregationCells.changeMenu.updateAggregationFromFile.buttonText') }}
    add-period-aggregation-cell(:period="period" :update="addUpdate")
      template(#activator="{ on, attrs }")
        v-list-item(v-on="on" v-bind="attrs")
          v-list-item-icon
            v-icon mdi-form-select
          v-list-item-content {{ $t('dcis.periods.aggregationCells.changeMenu.addAggregation.buttonText') }}
</template>

<script lang="ts">
import { defineComponent, PropType, ref } from '#app'
import { AddUpdateType, ResetUpdateType } from '~/composables'
import { PeriodType } from '~/types/graphql'
import UpdatePeriodAggregationCellsFromFile from '~/components/dcis/periods/UpdatePeriodAggregationCellsFromFile.vue'
import AddPeriodAggregationCell from '~/components/dcis/periods/AddPeriodAggregationCell.vue'

export default defineComponent({
  components: { AddPeriodAggregationCell, UpdatePeriodAggregationCellsFromFile },
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    fromFileUpdate: { type: Function as PropType<ResetUpdateType>, required: true },
    addUpdate: { type: Function as PropType<AddUpdateType>, required: true }
  },
  setup () {
    const active = ref<boolean>(false)

    const close = () => {
      active.value = false
    }

    return {
      active,
      close
    }
  }
})
</script>
