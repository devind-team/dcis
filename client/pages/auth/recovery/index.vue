<template lang="pug">
  bread-crumbs(:items="breadCrumbs")
    v-row
      v-col.mx-auto(lg="4" md="6" cols="12")
        v-alert(v-if="success" type="success") {{ t('successSendEmail') }}
        apollo-mutation(
          v-else
          v-slot="{ mutate, loading, error }"
          :mutation="require('~/gql/core/mutations/user/recovery_password.graphql')"
          :variables="{ email }"
          @done="recoveryPasswordDone"
          tag
        )
          validation-observer(v-slot="{ handleSubmit, invalid }" ref="recoveryForm" tag="div")
            form(@submit.prevent="handleSubmit(mutate)")
              v-card
                v-card-title {{ t('recoveryTitle') }}
                v-card-text
                  v-alert(type="error" :value="!!error" dismissible) {{ error }}
                  validation-provider(:name="t('email')" rules="required|email" v-slot="{ errors, valid }")
                    v-text-field(v-model="email" :label="t('email')" prepend-icon="mdi-email" :error-messages="errors" :success="valid" clearable)
                v-card-actions
                  v-spacer
                  v-btn(type="submit" :disabled="invalid" :loading="loading" color="success") {{ t('restoreAccess') }}
</template>

<script lang="ts">
import { camelCase } from 'scule'
import { Vue, Component } from 'vue-property-decorator'
import { MetaInfo } from 'vue-meta'
import { ValidationObserver } from 'vee-validate'
import { BreadCrumbsItem } from '~/types/devind'
import { ErrorFieldType, RecoveryPasswordMutation } from '~/types/graphql'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'

@Component<AuthRecovery>({
  middleware: 'guest',
  components: { BreadCrumbs },
  computed: {
    breadCrumbs (): BreadCrumbsItem [] {
      return [
        { text: this.t('login.signIn'), to: this.localePath({ name: 'auth-login' }), exact: true },
        { text: this.t('restoreAccessToAccount'), to: this.localePath({ name: 'auth-recovery' }), exact: true }
      ]
    }
  },
  head (): MetaInfo {
    return { title: this.t('restoreAccessToAccount') } as MetaInfo
  }
})
export default class AuthRecovery extends Vue {
  $refs!: {
    recoveryForm: InstanceType<typeof ValidationObserver>
  }

  readonly breadCrumbs!: BreadCrumbsItem[]
  private success: boolean = false
  private email: string = ''

  recoveryPasswordDone (
    { data: { recoveryPassword: { success, errors } } }: { data: RecoveryPasswordMutation }
  ): void {
    this.success = success
    if (!success) {
      this.$refs.recoveryForm.setErrors(errors.reduce(
        (a: { [key: string]: string[] }, c: ErrorFieldType) => {
          return { ...a, [this.t(camelCase(c.field)) as string]: c.messages }
        }, {}))
    }
  }

  /**
   * Получение перевода относильно локального пути
   * @param path
   * @param values
   * @return
   */
  t (path: string, values: any = undefined): string {
    return this.$t(`auth.${path}`, values) as string
  }
}
</script>
