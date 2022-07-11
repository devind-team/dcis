<template lang="pug">
bread-crumbs(:items="breadCrumbs")
  v-row
    v-col.mx-auto(lg="4" md="6" cols="12")
      v-alert(v-if="success" type="success" v-html="$t('auth.recovery.passwordChanged')")
      mutation-form(
        v-else
        @done="restorePasswordDone"
        :mutation="require('~/gql/core/mutations/user/restore_password.graphql')"
        :variables="{ token: $route.params.token, password }"
        :header="String($t('auth.recovery.setNewPasswordForAccount'))"
        :button-text="String($t('auth.recovery.setNewPassword'))"
        mutation-name="restorePassword"
        i18n-path="auth.recovery"
      )
        template(#form)
          validation-provider(
            v-slot="{ errors, valid }"
            :name="String($t('auth.recovery.password'))"
            rules="required|min:4"
            vid="password"
          )
            v-text-field(
              v-model="password"
              @click:append-outer="hiddenPassword = !hiddenPassword"
              :label="$t('auth.recovery.password')"
              :error-messages="errors"
              :success="valid"
              :append-outer-icon="hiddenPassword ? 'mdi-eye-off' : 'mdi-eye'"
              :type="hiddenPassword ? 'password' : 'text'"
              autocomplete="off"
              autofocus
              clearable
            )
          validation-provider(
            v-slot="{ errors, valid }"
            :name="String($t('auth.recovery.passwordConfirmation'))"
            rules="required|min:4|confirmed:password"
          )
            v-text-field(
              v-model="passwordConfirm"
              :label="$t('auth.recovery.passwordConfirmation')"
              :error-messages="errors"
              :success="valid"
              type="password"
              autocomplete="off"
              clearable
            )
</template>

<script lang="ts">
import { useNuxt2Meta } from '#app'
import { BreadCrumbsItem } from '~/types/devind'
import { RestorePasswordMutation } from '~/types/graphql'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import MutationForm from '~/components/common/forms/MutationForm.vue'

export default defineComponent({
  components: { MutationForm, BreadCrumbs },
  middleware: 'guest',
  setup () {
    const { t, localePath } = useI18n()

    useNuxt2Meta({ title: t('auth.recovery.changePassword') as string })

    const breadCrumbs = computed<BreadCrumbsItem[]>(() => ([
      { text: t('auth.recovery.signIn') as string, to: localePath({ name: 'auth-login' }), exact: true },
      { text: t('auth.recovery.changePassword') as string, to: localePath({ name: 'auth-recovery-token' }), exact: true }
    ]))

    const success = ref<boolean>(false)
    const password = ref<string>('')
    const passwordConfirm = ref<string>('')
    const hiddenPassword = ref<boolean>(true)

    const restorePasswordDone = ({ data: { restorePassword: { errors } } }: { data: RestorePasswordMutation }) => {
      success.value = !errors.length
    }

    return { breadCrumbs, success, password, passwordConfirm, hiddenPassword, restorePasswordDone }
  }
})
</script>
