<template lang="pug">
apollo-mutation(
  v-slot="{ mutate, loading, error }"
  @done="changeUserDone"
  :mutation="require('~/gql/core/mutations/user/change_user_props.graphql')"
  :variables="{ userId: user.id, email, firstName, lastName, sirName, birthday }"
  tag
)
  validation-observer(v-slot="{ handleSubmit, invalid }")
    form(@submit.prevent="handleSubmit(mutate)")
      v-row
        v-col(cols="12" md="3") {{ $t('profile.information') }}
        v-col(cols="12" md="9")
          v-alert(type="success" :value="successUpdate") {{ $t('mutationSuccess')}}
          v-alert(type="error" :value="!!error" dismissible) {{$t('mutationBusinessLogicError', { error: error})}}
          v-text-field(
            :value="personalLink"
            :label="$t('profile.personalLink')"
            readonly)
            template(#append-outer)
              v-tooltip(bottom)
                template(#activator="{ on }")
                  v-btn(v-on="on" @click="copy(personalLink)" icon)
                    v-icon mdi-content-copy
                span {{ $t('copy') }}
          v-text-field(:value="user.username" :label="$t('profile.username')" readonly)
          validation-provider(:name="$t('profile.email')" rules="required|email" v-slot="{ errors, valid }")
            v-text-field(v-model="email" :label="$t('profile.email')" :error-messages="errors" :success="valid")
          validation-provider(:name="$t('profile.lastName')" rules="required|min:2|max:30" v-slot="{ errors, valid }")
            v-text-field(v-model="lastName" :label="$t('profile.lastName')" :error-messages="errors" :success="valid")
          validation-provider(:name="$t('profile.firstName')" rules="required|min:2|max:30" v-slot="{ errors, valid }")
            v-text-field(v-model="firstName" :label="$t('profile.firstName')" :error-messages="errors" :success="valid")
          validation-provider(:name="$t('profile.sirName')" rules="required|min:2|max:30" v-slot="{ errors, valid }")
            v-text-field(v-model="sirName" :label="$t('profile.sirName')" :error-messages="errors" :success="valid")
          v-menu(
            v-model="menu"
            :close-on-content-click="false"
            bottom max-width="290px"
            transition="scale-transition"
            min-width="290px"
          )
            template(v-slot:activator="{ on }")
              validation-provider(
                :name="$t('profile.birthday')"
                rules="required"
                v-slot="{ errors, valid }"
                tag="div"
              )
                v-text-field(
                  v-on="on"
                  v-model="birthday"
                  :error-messages="errors"
                  :success="valid"
                  :label="$t('profile.birthday')"
                  readonly
                )
            v-date-picker(v-model="birthday" @input="menu = false")
      v-row
        v-col.text-right
          v-btn(:disabled="invalid" :loading="loading" type="submit" color="success") {{ $t('save') }}
</template>

<script lang="ts">
import { promiseTimeout, useClipboard } from '@vueuse/core'
import type { ComputedRef, PropType } from '#app'
import { computed, defineComponent, ref, Ref, toRef } from '#app'
import { useAuthStore } from '~/stores'
import { ChangeUserPropsMutationPayload, UserType } from '~/types/graphql'

type ChangeUserPropsResultMutation = { data: { changeUserProps: ChangeUserPropsMutationPayload } }

export default defineComponent({
  props: {
    user: { type: Object as PropType<UserType>, required: true }
  },
  setup (props) {
    const { copy } = useClipboard()
    const userStore = useAuthStore()
    const user: Ref<UserType> = toRef(userStore, 'user')

    const successUpdate: Ref<boolean> = ref<boolean>(false)
    const menu: Ref<boolean> = ref<boolean>(false)
    const lastName: Ref<string> = ref<string>(props.user.lastName)
    const firstName: Ref<string> = ref<string>(props.user.firstName)
    const sirName: Ref<string> = ref<string>(props.user.sirName)
    const email: Ref<string> = ref<string>(props.user.email)
    const birthday: Ref<string> = ref<string>(props.user.birthday)

    const personalLink: ComputedRef<string> = computed<string>(() => {
      const param: string = `/users/${props.user.id}`
      return process.client ? `${window.location.protocol}//${window.location.host}${param}` : param
    })

    const changeUserDone = ({ data: { changeUserProps: { success, user: updatedUser } } }: ChangeUserPropsResultMutation) => {
      if (success) {
        user.value = Object.assign(user.value, updatedUser)
        successUpdate.value = true
        promiseTimeout(2000).then(() => (successUpdate.value = false))
      }
    }

    return { successUpdate, menu, lastName, firstName, sirName, email, birthday, copy, personalLink, changeUserDone }
  }
})

</script>
