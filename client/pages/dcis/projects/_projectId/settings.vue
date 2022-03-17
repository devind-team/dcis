<template lang="pug">
  bread-crumbs(:items="bc")
    v-card
      v-row.align-center
        v-col(cols="12" md="3")
          v-card-title Настройки
          v-card-subtitle {{ project.name }}
        v-col(cols="12" md="8")
          v-alert(type="success" :value="successUpdate") {{ $t('mutationSuccess')}}
          v-alert(type="error" :value="!!error" dismissible) {{$t('mutationBusinessLogicError', { error: error})}}
      apollo-mutation(
        v-slot="{ mutate, loading, error }"
        @done="changeProjectDone"
        :mutation="require('~/gql/dcis/mutations/project/change_project.graphql')"
        :variables="{ id: project.id, name,  short, description, visibility, archive }"
        tag
      )
        validation-observer(v-slot="{ handleSubmit, invalid }")
          form(@submit.prevent="handleSubmit(mutate)")
            v-card-text
              validation-provider(v-slot="{ errors, valid }" :name="$t('dcis.projects.addProject.name')" rules="required|min:3|max:250")
                v-text-field(v-model="name" :label="$t('dcis.projects.addProject.name')" :error-messages="errors" :success="valid" counter)
              validation-provider(v-slot="{ errors, valid }" :name="$t('dcis.projects.addProject.short')" rules="required|min:3|max:30")
                v-text-field(v-model="short" :label="$t('dcis.projects.addProject.short')" :error-messages="errors" :success="valid" counter)
              validation-provider(v-slot="{ errors, valid }" :name="$t('dcis.projects.addProject.description')" rules="required|min:3|max:1023")
                v-textarea(v-model="description" :label="$t('dcis.projects.addProject.description')" :error-messages="errors" :success="valid" counter)
              v-row
                v-col(cols="12" md="2")
                  v-checkbox(v-model="visibility" :label="$t('dcis.projects.addProject.visibility')")
                v-col(cols="12" md="10")
                  v-checkbox(v-model="archive" :label="$t('dcis.projects.changeProject.archive')")
            v-card-actions
              v-row
                v-col
                  v-btn(color="error") Удалить проект
                v-col.text-right
                  v-btn(type="submit" color="success") Сохранить
</template>

<script lang="ts">
import type { ComputedRef, PropType, Ref } from '#app'
import { computed, defineComponent } from '#app'
import { promiseTimeout } from '@vueuse/core'
import { ProjectType, ChangeProjectMutationPayload } from '~/types/graphql'
import { BreadCrumbsItem } from '~/types/devind'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import { useI18n } from '~/composables'

type ChangeProjectResultMutation = { data: { changeProject: ChangeProjectMutationPayload } }

export default defineComponent({
  components: { BreadCrumbs },
  middleware: 'auth',
  props: {
    project: { type: Object as PropType<ProjectType>, required: true },
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true }
  },
  setup (props) {
    const { localePath } = useI18n()

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      { text: 'Настройки', to: localePath({ name: 'dcis-projects-projectId-settings' }), exact: true }
    ]))
    const project: Ref<ProjectType> = ref<ProjectType>(props.project)
    const name: Ref<string> = ref<string>(props.project.name)
    const short: Ref<string> = ref<string>(props.project.short)
    const description: Ref<string> = ref<string>(props.project.description)
    const visibility: Ref<boolean> = ref<boolean>(props.project.visibility)
    const archive: Ref<boolean> = ref<boolean>(props.project.archive)
    const successUpdate: Ref<boolean> = ref<boolean>(false)

    const changeProjectDone = ({ data: { changeProject: { success, project: updatedProject } } }: ChangeProjectResultMutation) => {
      if (success) {
        project.value = Object.assign(project.value, updatedProject)
        successUpdate.value = true
        promiseTimeout(2000).then(() => (successUpdate.value = false))
      }
    }

    return { bc, changeProjectDone, name, short, description, visibility, archive, successUpdate }
  }
})
</script>
