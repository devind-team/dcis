<template lang="pug">
  bread-crumbs(:items="breadCrumbs")
    v-row
      v-col.mx-auto(lg="4" md="6" cols="12")
        v-alert(v-if="success" type="success" v-html="$t('auth.recovery.passwordChanged')")
        apollo-mutation(
          v-else
          v-slot="{ mutate, loading, error }"
          :mutation="require('~/gql/core/mutations/user/restore_password.graphql')"
          :variables="{ token: $route.params.token, password }"
          @done="restorePasswordDone"
          tag
        )
          validation-observer(v-slot="{ handleSubmit, invalid }")
            v-form(@submit.prevent="handleSubmit(mutate)")
              v-card
                v-card-title {{ t('setNewPasswordForAccount') }}
                v-card-text
                  v-alert(v-if="error" type="error" dismissible) {{ error }}
                  v-alert(v-if="errors" type="error") {{ errors }}
                  validation-provider(
                    v-slot="{ errors, valid }"
                    :name="t('password')"
                    rules="required|min:4"
                    vid="password"
                  )
                    v-text-field(
                      v-model="password"
                      @click:append-outer="hiddenPassword = !hiddenPassword"
                      :label="t('password')"
                      :error-messages="errors"
                      :success="valid"
                      :append-outer-icon="hiddenPassword ? 'mdi-eye-off' : 'mdi-eye'"
                      :type="hiddenPassword ? 'password' : 'text'"
                      autocomplete="off"
                      clearable
                    )
                  validation-provider(
                    v-slot="{ errors, valid }"
                    :name="t('passwordConfirmation')"
                    rules="required|min:4|confirmed:password"
                  )
                    v-text-field(
                      v-model="passwordConfirm"
                      :label="t('passwordConfirmation')"
                      :error-messages="errors"
                      :success="valid"
                      type="password"
                      autocomplete="off"
                      clearable
                    )
                v-card-actions
                  v-spacer
                  v-btn(type="submit" :disabled="invalid" :loading="loading" color="success") {{ t('setNewPassword') }}
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'
import { MetaInfo } from 'vue-meta'
import { RestorePasswordMutation } from '~/types/graphql'
import { BreadCrumbsItem } from '~/types/devind'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'

@Component<RecoveryToken>({
  middleware: 'guest',
  components: { BreadCrumbs },
  computed: {
    breadCrumbs (): BreadCrumbsItem [] {
      return [
        { text: this.t('signIn'), to: this.localePath({ name: 'auth-login' }), exact: true },
        { text: this.t('changePassword'), to: this.localePath({ name: 'auth-recovery-token' }), exact: true }
      ]
    }
  },
  head (): MetaInfo {
    return { title: this.t('changePassword') } as MetaInfo
  }
})
export default class RecoveryToken extends Vue {
  private success: boolean = false
  private errors: string = ''
  private password: string = ''
  private passwordConfirm: string = ''
  hiddenPassword: boolean = true

  restorePasswordDone (
    { data: { restorePassword: { success, errors } } }: { data: RestorePasswordMutation }
  ): void {
    this.success = success
    if (!success) {
      this.errors = errors.reduce<string>((a, c) => (`${a} ${c!.messages}.`), '')!.trim()
    }
  }

  /**
   * Получение перевода относильно локального пути
   * @param path
   * @param values
   * @return
   */
  t (path: string, values: any = undefined): string {
    return this.$t(`auth.recovery.${path}`, values) as string
  }
}
</script>
