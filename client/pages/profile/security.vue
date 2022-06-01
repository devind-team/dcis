<template lang="pug">
  v-card
    v-card-title {{ $t('profile.security.name') }}
    v-card-text
      v-row
        v-col(cols="12" md="3") {{ $t('profile.security.changePassword') }}
        v-col(cols="12" md="9")
          v-alert(v-show="passwordSuccess" type="success") {{ $t('profile.security.passwordSuccess') }}
          mutation-form(
            @done="changePasswordDone"
            :mutation="require('~/gql/core/mutations/user/change_password.graphql')"
            :variables="{ password, passwordNew }"
            :button-text="String($t('change'))"
            mutation-name="changePassword"
            i18n-path="profile"
            flat
          )
            template(#form)
              validation-provider(:name="String($t('profile.password'))" rules="required|min:4|max:30" v-slot="{ errors, valid }")
                v-text-field(
                  v-model="password"
                  :label="$t('profile.password')"
                  :error-messages="errors"
                  :success="valid"
                  autocomplete="off"
                  type="password"
                  clearable
                )
              validation-provider(:name="String($t('profile.passwordNew'))" rules="required|min:4|max:30" v-slot="{ errors, valid }")
                v-text-field(
                  v-model="passwordNew"
                  @click:append="hiddenPassword = !hiddenPassword"
                  :label="$t('profile.passwordNew')"
                  :error-messages="errors"
                  :success="valid"
                  :append-icon="hiddenPassword ? 'mdi-eye-off' : 'mdi-eye'"
                  :type="hiddenPassword ? 'password' : 'text'"
                  autocomplete="off"
                  clearable
                )
              validation-provider(:name="String($t('profile.passwordReset'))" :rules="`required|confirmPassword:@${$t('profile.passwordNew')}`" v-slot="{ errors, valid }")
                v-text-field(
                  v-model="passwordConfirm"
                  :label="$t('profile.passwordReset')"
                  autocomplete="off"
                  type="password"
                  :error-messages="errors"
                  :success="valid"
                  clearable
                )
    v-card-text
      v-row
        v-col(cols="12" md="3") {{ $t('profile.security.activeSessions') }}
        v-col(cols="12" md="9")
          v-data-table(:headers="headers" :items="sessions" disable-pagination hide-default-footer)
            template(v-slot:item.date="{ item }") {{ $filters.dateTimeHM(item.date) }}
            template(v-slot:item.activity="{ item }") {{ item.history }}/{{ item.activity }}
    v-card-actions
      v-spacer
      v-btn(color="warning" @click="deleteSessionsMutate") {{ $t('profile.security.endSessions') }}
</template>

<script lang="ts">
import { DataTableHeader } from 'vuetify'
import { useMutation } from '@vue/apollo-composable'
import { useNuxt2Meta } from '#app'
import { useAuthStore } from '~/stores'
import { ChangePasswordMutationPayload, SessionsQuery, SessionsQueryVariables, SessionType } from '~/types/graphql'
import sessionQuery from '~/gql/core/queries/sessions.graphql'
import deleteSessions from '~/gql/core/mutations/user/delete_sessions.graphql'
import MutationForm from '~/components/common/forms/MutationForm.vue'

export default defineComponent({
  components: { MutationForm },
  middleware: 'auth',
  setup () {
    const { t } = useI18n()
    const authStore = useAuthStore()
    const user = toRef(authStore, 'user')
    useNuxt2Meta({ title: t('profile.security.tableHeaders.name') as string })

    const headers = computed<DataTableHeader[]>(() => ([
      { text: t('profile.security.tableHeaders.activity') as string, value: 'activity', align: 'center' },
      { text: t('profile.security.tableHeaders.ip') as string, value: 'ip' },
      { text: t('profile.security.tableHeaders.device') as string, value: 'device' },
      { text: t('profile.security.tableHeaders.os') as string, value: 'os' },
      { text: t('profile.security.tableHeaders.browser') as string, value: 'browser' },
      { text: t('profile.security.tableHeaders.date') as string, value: 'date' }
    ]))

    const password = ref<string>('')
    const passwordNew = ref<string>('')
    const passwordConfirm = ref<string>('')
    const hiddenPassword = ref<boolean>(true)
    const passwordSuccess = ref<boolean>(false)

    const changePasswordDone = ({ data: { changePassword } }: { data: { changePassword: ChangePasswordMutationPayload }}) => {
      if (!changePassword.errors.length) {
        password.value = passwordNew.value = passwordConfirm.value = ''
        passwordSuccess.value = true
        setTimeout(() => {
          passwordSuccess.value = false
        }, 5000)
      }
    }

    const { data: sessions, update } = useCommonQuery<SessionsQuery, SessionsQueryVariables>({
      document: sessionQuery,
      variables: () => ({
        userId: user.value.id
      })
    })

    const { mutate: deleteSessionsMutate } = useMutation(deleteSessions, {
      update: (cache, result) => update(cache, result, (dataCache) => {
        dataCache.sessions = dataCache.sessions.filter((session: SessionType) => session.id !== user.value.session.id)
        return dataCache
      })
    })

    return {
      password,
      passwordNew,
      passwordConfirm,
      hiddenPassword,
      passwordSuccess,
      changePasswordDone,
      headers,
      sessions,
      deleteSessionsMutate
    }
  }
})
</script>
