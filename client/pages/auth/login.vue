<template lang="pug">
  bread-crumbs(:items="breadCrumbs")
    v-row
      v-col.mx-auto(cols="12" sm="4" md="4")
        mutation-form(
          @done="tokenDone"
          :mutation="require('~/gql/core/mutations/user/get_token.graphql')"
          :variables="variables"
          :header="String($t('auth.login.signIn'))"
          i18n-path="auth.login"
          mutation-name="getToken"
        )
          template(#form)
            validation-provider(
              v-slot="{ errors, valid }"
              :name="String($t('auth.login.username'))"
              rules="required|min:2|max:50"
            )
              v-text-field(
                v-model="username"
                :label="$t('auth.login.username')"
                :error-messages="errors"
                :success="valid"
              )
            validation-provider(
              v-slot="{ errors, valid }"
              :name="String($t('auth.login.password'))"
              rules="required|min:8"
            )
              v-text-field(
                v-model="password"
                @click:append="hiddenPassword = !hiddenPassword"
                :label="$t('auth.login.password')"
                :error-messages="errors"
                :success="valid"
                :append-icon="hiddenPassword ? 'mdi-eye-off' : 'mdi-eye'"
                :type="hiddenPassword ? 'password' : 'text'"
                autocomplete="on"
              )
          template(#actions="{ invalid, loading }")
            v-btn(
              :loading="loading"
              :disabled="invalid"
              type="submit"
              color="success"
            ) {{ $t('auth.login.enter') }}
            v-spacer
            nuxt-link(:to="localePath({ name: 'auth-recovery' })") {{ $t('auth.login.forgotPassword') }}
</template>

<script lang="ts">
import type { ComputedRef, Ref } from '#app'
import {
  computed,
  defineComponent,
  ref,
  useNuxt2Meta,
  useNuxtApp,
  useRoute,
  useRouter,
  useRuntimeConfig
} from '#app'
import { useApolloHelpers, useI18n } from '~/composables'
import { GetTokenMutation, GetTokenMutationVariables, UserType } from '~/types/graphql'
import { useAuthStore } from '~/store/auth-store'
import { BreadCrumbsItem } from '~/types/devind'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import MutationForm from '~/components/common/forms/MutationForm.vue'

export default defineComponent({
  components: { MutationForm, BreadCrumbs },
  middleware: 'guest',
  setup () {
    const router = useRouter()
    const route = useRoute()
    const { $store } = useNuxtApp()
    const { t, localePath } = useI18n()
    const { onLogin, defaultClient } = useApolloHelpers()
    const authStore = useAuthStore()
    const { CLIENT_ID, CLIENT_SECRET } = useRuntimeConfig()

    useNuxt2Meta({ title: t('auth.login.signIn') as string })

    const username: Ref<string> = ref<string>('')
    const password: Ref<string> = ref<string>('')
    const loginError: Ref<string | null> = ref<string | null>(null)
    const hiddenPassword: Ref<boolean> = ref<boolean>(true)

    const breadCrumbs: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      { text: t('auth.login.signIn') as string, to: localePath({ name: 'auth-login' }), exact: true }
    ]))

    const variables: ComputedRef<GetTokenMutationVariables> = computed(() => ({
      clientId: CLIENT_ID,
      clientSecret: CLIENT_SECRET,
      grantType: 'password',
      username: username.value,
      password: password.value
    }))

    const tokenDone = ({ data: { getToken: { success, errors, accessToken, expiresIn, user } } }: { data: GetTokenMutation }) => {
      if (success) {
        onLogin(accessToken, defaultClient, { maxAge: expiresIn, path: '/' }, true)
        authStore.user = user as UserType

        // Убрать после удаления vuex
        $store.dispatch('auth/fetchExistUser', Object.assign({}, user))

        router.push((route.query.to as string) || '/')
      } else {
        loginError.value = errors[0].messages[0]
        setTimeout(() => { loginError.value = null }, 5000)
      }
    }
    return { breadCrumbs, username, password, loginError, hiddenPassword, variables, tokenDone }
  }
})

</script>
