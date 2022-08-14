import { defineStore } from 'pinia'
// import { acceptHMRUpdate } from 'pinia'
import { useCookies } from '@vueuse/integrations/useCookies'
import { useMutation } from '@vue/apollo-composable'
import { LogoutMutation, LogoutMutationVariables, UserType } from '~/types/graphql'
import logoutMutation from '~/gql/core/mutations/user/logout.graphql'

export type AuthStoreStateType = {
  user: UserType | null
}

export type HasPermissionFnType = (code: string | string[], or?: boolean) => boolean

export type AuthStoreGettersType = {
  loginIn: (state: any) => boolean,
  hasPerm: (state: any) => HasPermissionFnType
}

export type AuthStoreActionsType = {
  logout: () => void
}

export const useAuthStore = defineStore<string, AuthStoreStateType, AuthStoreGettersType, AuthStoreActionsType>('authStore', {
  state: () => ({
    user: null
  }),
  getters: {
    loginIn: state => state.user !== null,
    hasPerm (): HasPermissionFnType {
      return (code: string | string[], or: boolean = false): boolean => {
        if (!this.loginIn) { return false }
        if (Array.isArray(code)) {
          return or
            ? code.reduce((a, c) => (a || this.hasPerm(c)), false)
            : code.reduce((a, c) => (a && this.hasPerm(c)), true)
        } else {
          return Boolean(this.user.permissions!.includes(code))
        }
      }
    }
  },
  actions: {
    logout (): void {
      if (this.loginIn && this.user.session) {
        const { mutate } = useMutation<LogoutMutation, LogoutMutationVariables>(logoutMutation)
        mutate({ sessionId: this.user.session.id }).then()
        this.user = null
      }
    }
  }
})

// if (import.meta.hot) {
//   import.meta.hot.accept(acceptHMRUpdate(useAuthStore, import.meta.hot))
// }
