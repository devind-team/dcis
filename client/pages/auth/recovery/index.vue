<template lang="pug">
bread-crumbs(:items="breadCrumbs")
  v-row
    v-col.mx-auto(lg="4" md="6" cols="12")
      v-alert(v-if="success" type="success") {{ $t('auth.successSendEmail') }}
      mutation-form(
        @done="recoveryPasswordDone"
        v-else
        :mutation="require('~/gql/core/mutations/user/recovery_password.graphql')"
        :variables="{ email }"
        :header="String($t('auth.recoveryTitle'))"
        :button-text="String($t('auth.restoreAccess'))"
        i18n-path="auth"
        mutation-name="recoveryPassword"
      )
        template(#form)
          validation-provider(:name="String($t('auth.email'))" rules="required|email" v-slot="{ errors, valid }")
            v-text-field(v-model="email" :label="$t('auth.email')" prepend-icon="mdi-email" :error-messages="errors" :success="valid" clearable)
</template>

<script lang="ts">
import { useNuxt2Meta } from '#app'
import { BreadCrumbsItem } from '~/types/devind'
import { RecoveryPasswordMutation } from '~/types/graphql'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import MutationForm from '~/components/common/forms/MutationForm.vue'

export default defineComponent({
  components: { MutationForm, BreadCrumbs },
  middleware: 'guest',
  setup () {
    const { t, localePath } = useI18n()

    useNuxt2Meta({ title: t('auth.restoreAccessToAccount') as string })
    const breadCrumbs = computed<BreadCrumbsItem[]>(() => ([
      { text: t('auth.login.signIn') as string, to: localePath({ name: 'auth-login' }), exact: true },
      { text: t('auth.restoreAccessToAccount') as string, to: localePath({ name: 'auth-recovery' }), exact: true }
    ]))

    const email = ref<string>('')
    const success = ref<boolean>(false)

    const recoveryPasswordDone = ({ data: { recoveryPassword: { errors } } }: { data: RecoveryPasswordMutation }) => {
      success.value = !errors.length
    }

    return { email, success, breadCrumbs, recoveryPasswordDone }
  }
})
</script>
