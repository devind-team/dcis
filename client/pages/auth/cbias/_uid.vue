<template lang="pug">
bread-crumbs(:items="bc")
  v-row(v-if="result")
    v-col Подождите, идет авторизация.
      v-progress-circular(color="primary" indeterminate)
  v-row(v-else)
    v-col
      v-alert(type="warning") Авторизация не удалась, обратитесь к администратору портала.
</template>

<script lang="ts">
import { useMutation } from '@vue/apollo-composable'
import type { ComputedRef, Ref } from '#app'
import {
  ref,
  computed,
  defineComponent,
  useNuxt2Meta,
  useNuxtApp,
  useRoute,
  useRouter,
  useRuntimeConfig,
  onMounted
} from '#app'
import { useApolloHelpers, useI18n } from '~/composables'
import { useAuthStore } from '~/stores'
import { AuthCbiasMutation, AuthCbiasMutationVariables, UserType } from '~/types/graphql'
import { BreadCrumbsItem } from '~/types/devind'
import authCbiasMutation from '~/gql/dcis/mutations/auth_cbias.graphql'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'

export type AuthMutationResult = { data: AuthCbiasMutation }

export default defineComponent({
  components: { BreadCrumbs },
  middleware: 'guest',
  setup () {
    const { t, localePath } = useI18n()
    const router = useRouter()
    const route = useRoute()
    const { onLogin, defaultClient } = useApolloHelpers()
    const userStore = useAuthStore()
    const { CLIENT_ID, CLIENT_SECRET } = useRuntimeConfig()

    useNuxt2Meta({ title: t('auth.login.signIn') as string })

    const result: Ref<boolean> = ref<boolean>(true)

    const { mutate, onDone } = useMutation<AuthCbiasMutation, AuthCbiasMutationVariables>(authCbiasMutation)
    onMounted(() => {
      mutate({ uid: route.params.uid, clientId: CLIENT_ID, clientSecret: CLIENT_SECRET })
    })
    onDone(({ data: { authCbias: { success, token, user } } }: AuthMutationResult) => {
      result.value = success
      if (success) {
        onLogin(token.accessToken, defaultClient, { maxAge: token.expiresIn, path: '/' }, true)
        userStore.user = Object.assign({}, user) as UserType
        // Необходимо для нормальной перезагрузки сокетов
        router.push(localePath({ name: 'dcis-projects' }))
      }
    })

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      { text: t('auth.login.signIn') as string, to: localePath({ name: 'auth-login' }), exact: true },
      { text: 'Портал https://cbias.ru', to: localePath({ name: 'auth-cbias-uid', params: route.params }), exact: true }
    ]))
    return { result, bc }
  }
})
</script>
