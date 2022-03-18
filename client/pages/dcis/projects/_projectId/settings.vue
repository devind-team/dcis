<template lang="pug">
  bread-crumbs(:items="bc")
    apollo-mutation(
      v-slot="{ mutate, loading, error }"
      @done="changeProjectDone"
      :mutation="require('~/gql/dcis/mutations/project/change_project.graphql')"
      :variables="{ id: project.id, name,  short, description, visibility, archive }"
      tag
    )
      v-card
        v-row.align-center
          v-col(cols="12" md="3")
            v-card-title {{$t('dcis.projects.changeProject.header')}}
            v-card-subtitle {{ project.name }}
          v-col(cols="12" md="8")
            v-alert(type="success" :value="successUpdate") {{ $t('mutationSuccess')}}
            v-alert(type="error" :value="!!error" dismissible) {{$t('mutationBusinessLogicError', { error: error})}}
        validation-observer(v-slot="{ handleSubmit, invalid }")
          form(@submit.prevent="handleSubmit(mutate)")
            v-card-text
              validation-provider(
                v-slot="{ errors, valid }"
                :name="$t('dcis.projects.addProject.name')"
                rules="required|min:3|max:250"
              )
                v-text-field(
                  v-model="name"
                  :label="$t('dcis.projects.addProject.name')"
                  :error-messages="errors" :success="valid"
                  counter
                )
              validation-provider(
                v-slot="{ errors, valid }"
                :name="$t('dcis.projects.addProject.short')"
                rules="required|min:3|max:30"
              )
                v-text-field(
                  v-model="short"
                  :label="$t('dcis.projects.addProject.short')"
                  :error-messages="errors"
                  :success="valid"
                  counter
                )
              validation-provider(
                v-slot="{ errors, valid }"
                :name="$t('dcis.projects.addProject.description')"
                rules="required|min:3|max:1023"
              )
                v-textarea(
                  v-model="description"
                  :label="$t('dcis.projects.addProject.description')"
                  :error-messages="errors"
                  :success="valid"
                  counter
                )
              v-row
                v-col(cols="12" md="2")
                  v-checkbox(v-model="visibility" :label="$t('dcis.projects.addProject.visibility')")
                v-col(cols="12" md="10")
                  v-checkbox(v-model="archive" :label="$t('dcis.projects.changeProject.archive')")
            v-card-actions
              v-row
                v-col
                  apollo-mutation(
                    :mutation="require('~/gql/dcis/mutations/project/delete_project.graphql')"
                    :variables="{ id: project.id}"
                    @done="deleteProjectDone"
                  )
                    template(v-slot="{ mutate }")
                      delete-menu(
                        v-if="project.user === user || hasPerm('dcis.delete_project')"
                        v-slot="{ on }"
                        :itemName="$t('dcis.projects.changeProject.deleteItemName')"
                        @confirm="mutate"
                        @cancel="active = false"
                      )
                        v-btn(v-on="on" color="error") {{$t('dcis.projects.changeProject.delete')}}
                v-col.text-right
                  v-btn(
                    v-if="project.user === user || hasPerm('dcis.change_project')"
                    :disabled="invalid"
                    :loading="loading"
                    type="submit"
                    color="success"
                  ) {{$t('dcis.projects.changeProject.save')}}
</template>

<script lang="ts">
import type {ComputedRef, PropType, Ref } from '#app'
import { computed, defineComponent, toRefs, useRouter } from '#app'
import { promiseTimeout } from '@vueuse/core'
import { ChangeProjectMutationPayload, DeleteProjectMutationPayload, ProjectType, UserType} from '~/types/graphql'
import { BreadCrumbsItem } from '~/types/devind'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import { useI18n } from '~/composables'
import { HasPermissionFnType, useAuthStore } from '~/store'
import DeleteMenu from '~/components/common/menu/DeleteMenu.vue'

type ChangeProjectResultMutation = { data: { changeProject: ChangeProjectMutationPayload } }
type DeleteProjectResultMutation = { data: { deleteProject: DeleteProjectMutationPayload } }

export default defineComponent({
  components: { BreadCrumbs, DeleteMenu },
  middleware: 'auth',
  props: {
    project: { type: Object as PropType<ProjectType>, required: true },
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true }
  },
  setup (props) {
    const authStore = useAuthStore()
    const { localePath } = useI18n()
    const router = useRouter()
    const { user, hasPerm } = toRefs<{ user: UserType, hasPerm: HasPermissionFnType }>(authStore)

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
    const active: Ref<boolean> = ref<boolean>(false)

    const changeProjectDone = ({ data: { changeProject: { success, project: updatedProject } } }: ChangeProjectResultMutation) => {
      if (success) {
        project.value = Object.assign(project.value, updatedProject)
        successUpdate.value = true
        promiseTimeout(2000).then(() => (successUpdate.value = false))
      }
    }

    const deleteProjectDone = ({ data: { deleteProject: { success } } }: DeleteProjectResultMutation) => {
      if (success) {
        router.push(localePath({ name: 'dcis-projects' }))
      }
    }

    return {
      bc,
      changeProjectDone,
      name,
      short,
      description,
      visibility,
      archive,
      successUpdate,
      hasPerm,
      active,
      deleteProjectDone,
      user
    }
  }
})
</script>
