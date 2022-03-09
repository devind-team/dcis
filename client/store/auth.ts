import { GetterTree, MutationTree, ActionTree } from 'vuex'
import * as types from '~/store/mutation-types'
import {
  MeQuery,
  MeQueryVariables,
  UserType
} from '~/types/graphql'
import meQuery from '~/gql/core/queries/me.graphql'

export type HasPermissionFnType = (code: string | string[], or?: boolean) => boolean

export const state = () => ({
  user: null as UserType | null
})

export type AuthState = ReturnType<typeof state>

export const getters: GetterTree<AuthState, AuthState> = {
  user: state => state.user,
  loginIn: state => state.user !== null,
  hasPerm: (state, getters): HasPermissionFnType => (code: string | string[], or: boolean = false): boolean => {
    if (!getters.loginIn) { return false }
    if (Array.isArray(code)) {
      return or
        ? code.reduce((a, c) => (a || getters.hasPerm(c)), false)
        : code.reduce((a, c) => (a && getters.hasPerm(c)), true)
    } else {
      return Boolean(state.user!.permissions!.includes(code))
    }
  }
}

export const mutations: MutationTree<AuthState> = {
  [types.FETCH_USER] (state, user: UserType) {
    state.user = user
  },
  [types.LOGOUT] (state) {
    state.user = null
  },
  [types.CHANGE_USER_PROPS] (state, user: UserType) {
    state.user!.email = user.email
    state.user!.firstName = user.firstName as string
    state.user!.lastName = user.lastName as string
    state.user!.sirName = user.sirName as string
  },
  [types.CHANGE_USER_AVATAR] (state, avatar: string) {
    state.user!.avatar = avatar
  },
  [types.CHANGE_USER_VERIFICATION] (state, { email, agreement }: { email: string, agreement: string }) {
    state.user!.email = email
    state.user!.agreement = agreement
  }
}

export const actions: ActionTree<AuthState, AuthState> = {
  async fetchExistUser ({ commit }, user: UserType) {
    await commit(types.FETCH_USER, user)
  },
  async fetchUser ({ commit, dispatch }) {
    const user: UserType = await this.app.apolloProvider!.defaultClient.query<MeQuery, MeQueryVariables>({
      query: meQuery,
      fetchPolicy: 'network-only'
    }).then(({ data }) => data.me as UserType)
    user === null ? await dispatch('logout') : await commit(types.FETCH_USER, user)
  },
  async changeUserProps ({ commit }, payload: UserType) {
    await commit(types.CHANGE_USER_PROPS, payload)
  },
  async changeUserAvatar ({ commit }, avatar: string) {
    await commit(types.CHANGE_USER_AVATAR, avatar)
  },
  async changeVerification ({ commit }, payload: { email: string, agreement: string }) {
    await commit(types.CHANGE_USER_VERIFICATION, payload)
  },
  async logout ({ commit }) {
    await commit(types.LOGOUT)
  }
}
