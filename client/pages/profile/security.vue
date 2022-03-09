<template lang="pug">
  v-card
    v-card-title {{ t('name') }}
    v-card-text
      ValidationObserver(v-slot="{ invalid }" ref="passwordForm")
        form(@submit.prevent="saveChanges")
          v-row
            v-col(cols="12" md="3") {{ t('changePassword') }}
            v-col(cols="12" md="9")
              v-alert(v-if="passwordSuccess" type="success") {{ passwordSuccess }}
              v-alert(v-if="passwordError" type="error") {{ passwordError }}
              ValidationProvider(:name="$t('profile.password')" rules="required|min:4|max:30" v-slot="{ errors, valid }")
                v-text-field(
                  v-model="password"
                  :label="$t('profile.password')"
                  :error-messages="errors"
                  :success="valid"
                  autocomplete="off"
                  type="password"
                  clearable
                )
              ValidationProvider(:name="$t('profile.passwordNew')" rules="required|min:4|max:30" v-slot="{ errors, valid }")
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
              ValidationProvider(:name="$t('profile.passwordReset')" :rules="`required|confirmPassword:@${$t('profile.passwordNew')}`" v-slot="{ errors, valid }")
                v-text-field(
                  v-model="passwordConfirm"
                  :label="$t('profile.passwordReset')"
                  autocomplete="off"
                  type="password"
                  :error-messages="errors"
                  :success="valid"
                  clearable
                )
          v-row
            v-col.text-right
              v-btn(type="submit" color="success" :loading="changePasswordLoading" :disabled="invalid") {{ $t('change') }}
    v-card-text
      v-row
        v-col(cols="12" md="3") {{ t('activeSessions') }}
        v-col(cols="12" md="9")
          v-data-table(:headers="headers" :items="sessions" disable-pagination hide-default-footer)
            template(v-slot:item.date="{ item }") {{ $filters.dateTimeHM(item.date) }}
            template(v-slot:item.activity="{ item }") {{ item.history }}/{{ item.activity }}
    v-card-actions
      v-spacer
      v-btn(color="warning" @click="deleteSessions") {{ t('endSessions') }}
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'
import { MetaInfo } from 'vue-meta'
import { mapGetters } from 'vuex'
import { ValidationObserver } from 'vee-validate'
import { DataTableHeader } from 'vuetify/types'
import changePassword from '~/gql/core/mutations/user/change_password.graphql'
import deleteSessions from '~/gql/core/mutations/user/delete_sessions.graphql'
import sessionQuery from '~/gql/core/queries/sessions.graphql'
import {
  ChangePasswordMutation,
  ChangePasswordMutationVariables,
  DeleteSessionsMutation,
  DeleteSessionsMutationVariables, ErrorFieldType, SessionType, UserType
} from '~/types/graphql'

@Component<ProfileSecurityPage>({
  middleware: 'auth',
  computed: {
    ...mapGetters({ user: 'auth/user' }),
    headers (): DataTableHeader[] {
      return [
        { text: this.t('tableHeaders.activity'), value: 'activity', align: 'center' },
        { text: this.t('tableHeaders.ip'), value: 'ip' },
        { text: this.t('tableHeaders.device'), value: 'device' },
        { text: this.t('tableHeaders.os'), value: 'os' },
        { text: this.t('tableHeaders.browser'), value: 'browser' },
        { text: this.t('tableHeaders.date'), value: 'date' }
      ]
    }
  },
  apollo: {
    sessions: { query: sessionQuery, variables () { return { userId: this.user.id } } }
  },
  head (): MetaInfo { return { title: this.t('name') } as MetaInfo }
})
export default class ProfileSecurityPage extends Vue {
  $refs!: { passwordForm: InstanceType<typeof ValidationObserver> }

  sessions!: SessionType[]
  user!: UserType
  headers!: DataTableHeader[]

  password: string = ''
  passwordNew: string = ''
  passwordConfirm: string = ''
  passwordSuccess: string = ''
  passwordError: string = ''
  changePasswordLoading: boolean = false
  hiddenPassword: boolean = true

  /**
   * Получение перевода относильно локального пути
   * @param path
   * @param values
   * @return
   */
  t (path: string, values: any = undefined): string {
    return this.$t(`profile.security.${path}`, values) as string
  }

  async saveChanges () {
    this.changePasswordLoading = true
    await this.$apollo.mutate<ChangePasswordMutation, ChangePasswordMutationVariables>({
      mutation: changePassword,
      variables: {
        password: this.password,
        passwordNew: this.passwordNew
      },
      update: (_: any, { data: { changePassword: { success, errors } } }: any) => {
        if (success) {
          this.password = this.passwordNew = this.passwordConfirm = ''
          this.$nextTick(() => { this.$refs.passwordForm.reset() })
          this.passwordSuccess = this.t('passwordSuccess')
          setTimeout(() => { this.passwordSuccess = '' }, 5000)
        } else {
          this.passwordError = (errors as ErrorFieldType[]).reduce<string[]>((a: string[], c: ErrorFieldType) => a.concat(c.messages), []).join(', ')
          setTimeout(() => { this.passwordError = '' }, 5000)
        }
      }
    })
    this.changePasswordLoading = false
  }

  async deleteSessions () {
    await this.$apollo.mutate<DeleteSessionsMutation, DeleteSessionsMutationVariables>({
      mutation: deleteSessions,
      update: (store: any) => {
        const data: any = store.readQuery({ query: sessionQuery, variables: { userId: this.user.id } })
        data.sessions = data.sessions.filter((session: SessionType) => session.id === this.user.session!.id)
        store.writeQuery({ query: sessionQuery, variables: { userId: this.user.id }, data })
      }
    })
  }
}
</script>
