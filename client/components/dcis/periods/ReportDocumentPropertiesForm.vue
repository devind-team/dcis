<template lang="pug">
v-dialog(v-model="active" width="578")
  template(#activator="{ on, attrs }")
    slot(name="activator" :on="on" :attrs="attrs")
  form(@submit.prevent="save")
    v-card
      v-card-title {{ $t('dcis.periods.report.documentsFilter.propertiesForm.header') }}
        v-spacer
        v-btn(@click="close" icon)
          v-icon mdi-close
      v-card-subtitle {{ $t('dcis.periods.report.documentsFilter.propertiesForm.subheader', { divisionId: document.objectId }) }}
      v-card-text
        v-switch(
          v-model="isVisibleLocal"
          :label="$t('dcis.periods.report.documentsFilter.propertiesForm.isVisible')"
        )
        v-switch(
          v-model="isColored"
          :label="$t('dcis.periods.report.documentsFilter.propertiesForm.color')"
        )
        v-color-picker(
          v-if="isColored"
          v-model="colorLocal"
          :swatches="swatches"
          width="546"
          swatches-max-height="180"
          hide-canvas
          show-swatches
        )
      v-card-actions
        v-spacer
        v-btn(
          type="submit"
          color="primary"
        ) {{ $t('dcis.periods.report.documentsFilter.propertiesForm.buttonText') }}
</template>

<script lang="ts">
import { defineComponent, ref, PropType } from '#app'
import { DocumentType } from '~/types/graphql'

export default defineComponent({
  props: {
    document: { type: Object as PropType<DocumentType>, required: true },
    isVisible: { type: Boolean, required: true },
    color: { type: String, default: null }
  },
  setup (props, { emit }) {
    const active = ref<boolean>(false)

    const isVisibleLocal = ref<boolean>(props.isVisible)
    const isColored = ref<boolean>(!!props.color)
    const colorLocal = ref<string>(props.color || '#5A83C3')

    const swatches = [
      ['#821506', '#DAB9B0', '#C8816D', '#B2492B', '#8F2709', '#732611', '#4E1403'],
      ['#DC2B11', '#E9CDCC', '#D79C9A', '#C76B67', '#AF200B', '#831506', '#570B02'],
      ['#E79D2A', '#F6E6CF', '#EDCCA0', '#E5B472', '#D29444', '#A1621B', '#6B4110'],
      ['#FEFF46', '#FBF3CF', '#F8E69F', '#F4DA72', '#E4C448', '#B39225', '#776115'],
      ['#90FD43', '#DEEAD4', '#C0D7AB', '#A3C382', '#7FA757', '#4F7529', '#354E1A'],
      ['#92FCFE', '#D5E0E3', '#ADC3C9', '#86A4AE', '#5B808D', '#2E4E5B', '#1D333C'],
      ['#6284E3', '#CED9F6', '#AEC1F1', '#7F9CE7', '#5476D4', '#3353C7', '#2D4484'],
      ['#1400F8', '#D5E1F2', '#ABC4E6', '#83A7D9', '#5A83C3', '#2F5191', '#1E3661'],
      ['#8506F8', '#D7D2E8', '#B1A7D4', '#8A7CC0', '#614EA3', '#301B72', '#1D124B'],
      ['#DD25F9', '#E3D2DB', '#C9A7BC', '#B27D9E', '#945077', '#642046', '#41142F']
    ]

    const save = () => {
      active.value = false
      emit('update:isVisible', isVisibleLocal.value)
      if (isColored.value) {
        emit('update:color', colorLocal.value)
      } else {
        emit('update:color', null)
        colorLocal.value = '#5A83C3'
      }
    }

    const close = () => {
      active.value = false
      isVisibleLocal.value = props.isVisible
      isColored.value = Boolean(props.color)
      colorLocal.value = props.color || '#5A83C3'
    }

    return { active, isVisibleLocal, isColored, colorLocal, swatches, save, close }
  }
})
</script>
