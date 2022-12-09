<template lang="pug">
v-menu(v-model="active" transition="slide-y-transition" offset-y left)
  template(#activator="{ on, attrs }")
    slot(name="activator" :on="on" :attrs="attrs")
  v-list(dense)
    update-period-limitations-from-file(:period="period" :update="fromFileUpdate")
      template(#activator="{ on, attrs }")
        v-list-item(v-on="on" v-bind="attrs")
          v-list-item-icon
            v-icon mdi-file
          v-list-item-content {{ $t('dcis.periods.limitations.changeMenu.updateLimitationFromFile.buttonText') }}
    add-period-limitation(:period="period" :update="addUpdate")
      template(#activator="{ on, attrs }")
        v-list-item(v-on="on" v-bind="attrs")
          v-list-item-icon
            v-icon mdi-form-select
          v-list-item-content {{ $t('dcis.periods.limitations.changeMenu.addLimitation.buttonText') }}
</template>

<script lang="ts">
import { defineComponent, PropType, ref } from '#app'
import { AddUpdateType, ResetUpdateType } from '~/composables'
import { PeriodType } from '~/types/graphql'
import AddPeriodLimitation from '~/components/dcis/periods/AddPeriodLimitation.vue'
import UpdatePeriodLimitationsFromFile from '~/components/dcis/periods/UpdatePeriodLimitationsFromFile.vue'

export default defineComponent({
  components: { UpdatePeriodLimitationsFromFile, AddPeriodLimitation },
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

    return { active, close }
  }
})
</script>
