<template lang="pug">
  mutation-modal-form(
    :header="$t('ac.teams.teamActions.unloadUsers.header')"
    :subheader="team.name"
    :buttonText="$t('ac.teams.teamActions.unloadUsers.buttonText')"
    :mutation="require('~/gql/core/mutations/user/unload_users.graphql')"
    :variables="{ extension: 'html', usersId: selectedJobs.map((e) => e.user.id), teamId: team.id }"
    mutation-name="unloadUsers"
    width="1000"
    errors-in-alert
    @done="unloadUsersDone"
    @close="close"
  )
    template(#activator="{ on }")
      slot(:on="on")
    template(#form)
      v-text-field(v-model="search" :label="$t('ac.teams.search')" prepend-icon="mdi-magnify" clearable)
      validation-provider(rules="required")
        v-data-table.mb-3(
          v-model="selectedJobs"
          :headers="headers"
          :items="team.jobs"
          :search="search"
          item-key="user.id"
          disable-pagination
          hide-default-footer
          show-select
        )
          template(#item.user.avatar="{ item }")
            avatar-dialog(:item="item.user")
          template(#item.user.username="{ item }")
            v-tooltip(bottom)
              template(#activator="{ on }")
                span(v-on="on") {{ item.user.username }}
              span {{ item.user.email }}
</template>

<script lang="ts">
import { DataTableHeader } from 'vuetify/types'
import { computed, defineComponent, Ref } from '#app'
import type { ComputedRef, PropType } from '#app'
import { useDebounceSearch, useI18n } from '~/composables'
import { JobType, TeamType, UnloadUsersMutationPayload } from '~/types/graphql'
import AvatarDialog from '~/components/users/AvatarDialog.vue'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'

type UnloadUsersData = { data: { unloadUsers: UnloadUsersMutationPayload } }

export default defineComponent({
  components: { MutationModalForm, AvatarDialog },
  props: {
    team: { type: Object as PropType<TeamType>, required: true }
  },
  setup () {
    const { t } = useI18n()
    const headers: ComputedRef<DataTableHeader[]> = computed<DataTableHeader[]>(() => ([
      { text: t('ac.teams.teamActions.unloadUsers.tableHeaders.avatar') as string, value: 'user.avatar' },
      { text: t('ac.teams.teamActions.unloadUsers.tableHeaders.username') as string, value: 'user.username' },
      { text: t('ac.teams.teamActions.unloadUsers.tableHeaders.lastName') as string, value: 'user.lastName' },
      { text: t('ac.teams.teamActions.unloadUsers.tableHeaders.firstName') as string, value: 'user.firstName' },
      { text: t('ac.teams.teamActions.unloadUsers.tableHeaders.sirName') as string, value: 'user.sirName' }
    ]))
    const { search } = useDebounceSearch()
    const selectedJobs: Ref<JobType[]> = ref<JobType[]>([])
    const unloadUsersDone = ({ data: { unloadUsers: { success, src } } }: UnloadUsersData) => {
      if (success) {
        window.open(`/${src}`, '_blank')
      }
    }
    const close = () => {
      search.value = ''
      selectedJobs.value = []
    }
    return { headers, search, selectedJobs, unloadUsersDone, close }
  }
})
</script>
