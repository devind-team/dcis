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
    v-list-item
      v-list-item-icon
        v-icon mdi-form-select
      v-list-item-content {{ $t('dcis.periods.limitations.changeMenu.addLimitation.buttonText') }}
</template>

<script lang="ts">
import { defineComponent, PropType, ref } from '#app'
import { ResetUpdateType } from '~/composables'
import { PeriodType } from '~/types/graphql'
import UpdatePeriodLimitationsFromFile from '~/components/dcis/periods/UpdatePeriodLimitationsFromFile.vue'

export default defineComponent({
  components: { UpdatePeriodLimitationsFromFile },
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    fromFileUpdate: { type: Function as PropType<ResetUpdateType>, required: true }
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
