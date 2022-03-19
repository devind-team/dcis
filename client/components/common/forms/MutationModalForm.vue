<template lang="pug">
  v-dialog(v-model="active" :width="width" :fullscreen="fullscreen" :persistent="persistent" scrollable)
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
import { VueConstructor } from 'vue'
import type { Ref, ComputedRef } from '#app'
import { computed, defineComponent, getCurrentInstance, ref } from '#app'
import MutationForm from '~/components/common/forms/MutationForm.vue'

type MutateFormType = InstanceType<typeof MutationForm> | null

export default defineComponent({
  components: { MutationForm },
  inheritAttrs: false,
  props: {
    mutationName: { type: String, required: true },
    successClose: { type: Boolean, default: true },
    errorsInAlert: { type: Boolean, default: false },
    fullscreen: { type: Boolean, default: false },
    persistent: { type: Boolean, default: false },
    canMinimize: { type: Boolean, default: false },
    header: { type: String, default: '' },
    subheader: { type: String, default: '' },
    buttonText: { type: String, default: '' },
    i18nPath: { type: String, default: '' },
    width: { type: [String, Number], default: 600 },
    hideAlertTimeout: { type: Number, default: 2000 }
  },
  setup (props, { emit }) {
    const instance = getCurrentInstance()
    const vm = instance?.proxy || instance as unknown as InstanceType<VueConstructor>
    // @ts-ignore: TS2322
    const mutationForm: Ref<MutateFormType> = ref<MutateFormType>(null)
    const active: Ref<boolean> = ref<boolean>(false)

    const mutationListeners: ComputedRef = computed(() => (
      Object.assign({}, vm.$listeners, {
        done (result: any) {
          const { success } = result.data[props.mutationName]
          if (success && props.successClose) {
            close()
          }
          emit('done', result)
        }
      })
    ))

    const close = () => {
      active.value = false
      mutationForm.value.clear()
      emit('close')
    }

    return { active, mutationForm, mutationListeners, close }
  }
})
</script>
