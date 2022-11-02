<template lang="pug">
mutation-modal-form(
  :header="String($t('dcis.periods.addPeriod.header'))"
  :subheader="project.name"
  :button-text="String($t('dcis.periods.addPeriod.buttonText'))"
  :mutation="addPeriod"
  :variables="variables"
  :update="addPeriodUpdate"
  mutation-name="addPeriod"
  i18n-path="dcis.periods.addPeriod"
  @close="close"
)
  template(#activator="{ on }")
    slot(name="activator" :on="on")
  template(#form)
    validation-provider(
      v-slot="{ errors, valid }"
      :name="String($t('dcis.periods.addPeriod.name'))"
      rules="required|min:3|max:250"
    )
      v-text-field(
        v-model="name"
        :label="$t('dcis.periods.addPeriod.name')"
        :error-messages="errors"
        :success="valid"
        autofocus
      )
    validation-provider(
      v-slot="{ errors, valid }"
      :name="String($t('dcis.periods.addPeriod.xlsxFile'))"
      rules="required"
    )
      v-file-input(
        v-model="xlsxFile"
        :label="$t('dcis.periods.addPeriod.xlsxFile')"
        :error-messages="errors"
        :success="valid"
        accept=".xlsx"
      )
    validation-provider(
      v-slot="{ errors }"
      :name="String($t('dcis.periods.addPeriod.limitationsFile'))"
    )
      v-file-input(
        v-model="limitationsFile"
        :label="$t('dcis.periods.addPeriod.limitationsFile')"
        :error-messages="errors"
        accept=".json"
      )
        template(#append-outer)
          v-tooltip(bottom)
            template(#activator="{ on, attrs }")
              v-btn(v-bind="attrs" v-on="on" href="/templates/Ограничения.json" small icon download)
                v-icon mdi-file-download
            span {{ $t('dcis.periods.addPeriod.downloadTemplate') }}
    v-checkbox(v-model="readonlyFillColor" :label="$t('dcis.periods.addPeriod.readonlyFillColor')")
    v-checkbox(
      v-if="project.contentType.model === 'department'"
      v-model="multiple"
      :label="$t('dcis.periods.addPeriod.multiple')"
    )
    v-checkbox(v-model="versioning" :label="$t('dcis.periods.addPeriod.versioning')")
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import type { PropType } from '#app'
import { defineComponent, ref } from '#app'
import { AddPeriodMutationVariables, AddPeriodMutationPayload, ProjectType } from '~/types/graphql'
import addPeriod from '~/gql/dcis/mutations/period/add_period.graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'

export type AddPeriodMutationResult = { data: { addPeriod: AddPeriodMutationPayload } }
type UpdateFunction = (cache: DataProxy | any, result: AddPeriodMutationPayload | any) => DataProxy | any

export default defineComponent({
  components: { MutationModalForm },
  props: {
    project: { type: Object as PropType<ProjectType>, required: true },
    update: { type: Function as PropType<UpdateFunction>, required: true }
  },
  setup (props) {
    const name = ref<string>('')
    const xlsxFile = ref<File | null>(null)
    const limitationsFile = ref<File | null>(null)
    const readonlyFillColor = ref<boolean>(false)
    const multiple = ref<boolean>(true)
    const versioning = ref<boolean>(false)

    const variables = computed<AddPeriodMutationVariables>(() => ({
      name: name.value,
      projectId: props.project.id,
      multiple: multiple.value,
      versioning: versioning.value,
      readonlyFillColor: readonlyFillColor.value,
      xlsxFile: xlsxFile.value,
      limitationsFile: limitationsFile.value
    }))

    const addPeriodUpdate = (cache: DataProxy, result: AddPeriodMutationResult) => {
      const { success } = result.data.addPeriod
      if (success) {
        props.update(cache, result)
      }
    }

    const close = () => {
      name.value = ''
      xlsxFile.value = null
      limitationsFile.value = null
    }

    return {
      name,
      xlsxFile,
      limitationsFile,
      readonlyFillColor,
      multiple,
      versioning,
      variables,
      addPeriod,
      addPeriodUpdate,
      close
    }
  }
})
</script>
