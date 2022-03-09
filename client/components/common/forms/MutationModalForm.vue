<template lang="pug">
  v-dialog(v-model="active" :width="width" :fullscreen="fullscreen" scrollable)
    template(#activator="{ on }")
      slot(name="activator" :on="on" :close="close")
    mutation-form(
      ref="mutationForm"
      v-bind="$attrs"
      :mutation-name="mutationName"
      :errors-in-alert="errorsInAlert"
      :header="header"
      :subheader="subheader"
      :button-text="buttonText"
      :i18n-path="i18nPath"
      :hide-alert-timeout="hideAlertTimeout"
      v-on="mutationListeners"
    )
      template(#header)
        slot(name="header" :header="header")
          span {{ header }}
        v-spacer
        v-btn(v-if="canMinimize" @click="active = false" icon)
          v-icon mdi-minus
        v-btn(@click="close" icon)
          v-icon mdi-close
      template(#subheader)
        slot(name="subheader" :subheader="subheader")
          span {{ subheader }}
      template(#form)
        slot(name="form")
      template(#actions="{ invalid, loading, buttonText, setFormErrors, setError, setSuccess }")
        slot(
          name="actions"
          :button-text="buttonText"
          :invalid="invalid"
          :loading="loading"
          :set-form-errors="setFormErrors"
          :set-error="setError"
          :set-success="setSuccess"
        )
          v-spacer
          v-btn(:disabled="invalid" :loading="loading" type="submit" color="primary") {{ buttonText }}
</template>

<script lang="ts">
import { Vue, Component, Prop, Ref } from 'vue-property-decorator'
import MutationForm from '~/components/common/forms/MutationForm.vue'

@Component<MutationModalForm>({
  components: { MutationForm },
  inheritAttrs: false,
  computed: {
    mutationListeners () {
      const vm = this
      return Object.assign({}, this.$listeners, {
        done (result: any) {
          const { success } = result.data[vm.mutationName]
          if (success && vm.successClose) {
            vm.close()
          }
          vm.$emit('done', result)
        }
      })
    }
  }
})
export default class MutationModalForm extends Vue {
  @Prop({ type: String, required: true }) readonly mutationName!: string
  @Prop({ type: Boolean, default: true }) readonly successClose!: string
  @Prop({ type: Boolean, default: false }) readonly errorsInAlert!: boolean
  @Prop({ type: Boolean, default: false }) readonly fullscreen!: boolean
  @Prop({ type: Boolean, default: false }) readonly canMinimize!: boolean
  @Prop({ type: String, default: '' }) readonly header!: string
  @Prop({ type: String, default: '' }) readonly subheader!: string
  @Prop({ type: String, default: '' }) readonly buttonText!: string
  @Prop({ type: String, default: '' }) readonly i18nPath!: string
  @Prop({ type: [Number, String], default: 600 }) readonly width!: number | string
  @Prop({ type: Number, default: 20000 }) readonly hideAlertTimeout!: number

  @Ref() readonly mutationForm!: InstanceType<typeof MutationForm>

  readonly mutationListeners!: Function[]

  active: boolean = false

  /**
   * Закрытие модального окна
   */
  close (): void {
    this.active = false
    this.mutationForm.clear()
    this.$emit('close')
  }
}
</script>
