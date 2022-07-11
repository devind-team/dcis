<template lang="pug">
bread-crumbs(:items="breadCrumbs")
  v-row(justify="center")
    v-col(cols="12" sm="10" md="8" lg="6")
      .text-h4.mb-2 {{ $t('user.verification.title') }}
      v-stepper(v-model="step" vertical)
        v-stepper-step(:complete="step > 1" step="1") {{ $t('user.verification.email') }}
        v-stepper-content(step="1")
          mutation-form(
            @done="requestCodeDone"
            :mutation="require('~/gql/core/mutations/user/request_code.graphql')"
            :variables="{ email }"
            mutation-name="requestCode"
            i18n-path="user.verification"
            button-text="Отправить код"
          )
            template(#form)
              validation-provider(v-slot="{ errors, valid }" :name="String($t('user.verification.email'))" rules="required|email")
                v-text-field(
                  v-model="email"
                  :label="$t('user.verification.email')"
                  :error-messages="errors"
                  :success="valid"
                  clearable
                )
        v-stepper-step(:complete="step > 2" step="2") {{ $t('user.verification.code') }}
        v-stepper-content(step="2")
          mutation-form(
            @done="confirmEmailDone"
            :mutation="require('~/gql/core/mutations/user/confirm_email.graphql')"
            :variables="{ email, code }"
            mutation-name="confirmEmail"
            i18n-path="user.verification"
          )
            template(#form)
              validation-provider(v-slot="{ errors, valid }" :name="String($t('user.verification.code'))" rules="required")
                v-text-field(v-model="code" :label="$t('user.verification.code')" :error-messages="errors" :success="valid" clearable)
            template(#actions="{ invalid, loading }")
              v-btn(type="submit" :disabled="invalid" :loading="loading" color="success") {{ $t('user.verification.confirm') }}
              v-spacer
              a(@click="reRequestCode") {{ time > 0 ? $t('user.verification.reRequestCodeTimer', { time }) : $t('user.verification.reRequestCode') }}
        v-stepper-step(:complete="step > 3" step="3") {{ $t('user.verification.confirmSuccess') }}
        v-stepper-content(step="3")
          v-card
            v-card-text
              v-alert(type="success") {{ $t('user.verification.confirmText', { email }) }}
</template>

<script lang="ts">
import { useNuxt2Meta } from '#app'
import { useAuthStore } from '~/stores'
import { ConfirmEmailMutation, RequestCodeMutation } from '~/types/graphql'
import { BreadCrumbsItem } from '~/types/devind'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import MutationForm from '~/components/common/forms/MutationForm.vue'

export const REQUEST_TIME = 60

export default defineComponent({
  components: { BreadCrumbs, MutationForm },
  setup () {
    const router = useRouter()
    const { t, localePath } = useI18n()
    const authStore = useAuthStore()

    useNuxt2Meta({ title: t('user.verification.title') as string })

    const breadCrumbs = computed<BreadCrumbsItem[]>(() => ([
      { text: t('user.verification.title') as string, to: localePath({ name: 'auth-verification' }), exact: true }
    ]))

    const time = ref<number>(REQUEST_TIME)
    const timer = ref<any | null>(null)
    const step = ref<number>(1)
    const email = ref<string>('')
    const code = ref<string>('')

    const reRequestCode = () => {
      if (time.value > 0) { return }
      step.value = 1
      time.value = REQUEST_TIME
      resetRequestCode()
    }

    const resetRequestCode = () => {
      if (timer.value) {
        clearInterval(timer.value)
      }
    }
    onDeactivated(resetRequestCode)

    const requestCodeDone = ({ data: { requestCode: { errors } } }: { data: RequestCodeMutation }) => {
      if (!errors.length) {
        step.value = 2
        timer.value = setInterval(() => { --time.value }, 1000)
        time.value = REQUEST_TIME
      }
    }

    const confirmEmailDone = ({ data: { confirmEmail: { errors, user } } } : { data: ConfirmEmailMutation }) => {
      if (!errors.length) {
        authStore.user = Object.assign(authStore.user, user)
        step.value = 3
        setTimeout(() => {
          router.push(localePath({ name: 'index' }))
        }, 2000)
      }
    }

    return { time, step, email, code, breadCrumbs, reRequestCode, requestCodeDone, confirmEmailDone }
  }
})
</script>
