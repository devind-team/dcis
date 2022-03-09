<template lang="pug">
  bread-crumbs(:items="breadCrumbs")
    v-row(justify="center")
      v-col(cols="12" sm="10" md="8" lg="6")
        .text-h4.mb-2 {{ t('title') }}
        v-stepper(v-model="step" vertical)
          v-stepper-step(:complete="step > 1" step="1") {{ t('email') }}
          v-stepper-content(step="1")
            apollo-mutation(
              v-slot="{ mutate, loading, error }"
              :mutation="require('~/gql/core/mutations/user/request_code.graphql')"
              :variables="{ email }"
              @done="doneRequestCode"
              tag
            )
              validation-observer(v-slot="{ handleSubmit, invalid }" ref="requestCodeForm" tag="div")
                form(@submit.prevent="handleSubmit(mutate)")
                  v-card
                    v-card-text
                      v-alert(type="error" :value="!!error" dismissible) {{ error }}
                      validation-provider(v-slot="{ errors, valid }" :name="t('email')" rules="required|email")
                        v-text-field(
                          v-model="email"
                          :label="t('email')"
                          :error-messages="errors"
                          :success="valid"
                          clearable
                        )
                    v-card-actions
                      v-btn(:disabled="invalid" :loading="loading" type="submit" color="success") Отправить код
          v-stepper-step(:complete="step > 2" step="2") {{ t('code') }}
          v-stepper-content(step="2")
            apollo-mutation(
              v-slot="{ mutate, loading, error }"
              :mutation="require('~/gql/core/mutations/user/confirm_email.graphql')"
              :variables="{ email, code }"
              @done="doneConfirmEmail"
              tag
            )
              validation-observer(v-slot="{ handleSubmit, invalid }" ref="confirmEmailForm" tag="div")
                form(@submit.prevent="handleSubmit(mutate)")
                  v-card
                    v-card-text
                      v-alert(type="error" :value="!!error" dismissible) {{ error }}
                      validation-provider(v-slot="{ errors, valid }" :name="t('code')" rules="required")
                        v-text-field(v-model="code" :label="t('code')" :error-messages="errors" :success="valid" clearable)
                    v-card-actions
                      v-btn(type="submit" :disabled="invalid" :loading="loading" color="success") {{ t('confirm') }}
                      v-spacer
                      a(@click="reRequestCode") {{ time > 0 ? t('reRequestCodeTimer', { time }) : t('reRequestCode') }}
          v-stepper-step(:complete="step > 3" step="3") {{ t('confirmSuccess') }}
          v-stepper-content(step="3")
            v-card
              v-card-text
                v-alert(type="success") {{ t('confirmText', { email }) }}
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'
import { MetaInfo } from 'vue-meta'
import { ValidationObserver } from 'vee-validate'
import { BreadCrumbsItem } from '~/types/devind'
import { ConfirmEmailMutation, ErrorFieldType, RequestCodeMutation } from '~/types/graphql'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'

@Component<Verification>({
  components: { BreadCrumbs },
  computed: {
    breadCrumbs (): BreadCrumbsItem [] {
      return [
        { text: this.t('title'), to: this.localePath({ name: 'auth-verification' }), exact: true }
      ]
    }
  },
  head (): MetaInfo {
    return { title: this.t('title') } as MetaInfo
  }
})
export default class Verification extends Vue {
  readonly breadCrumbs!: BreadCrumbsItem[]
  $refs!: {
    requestCodeForm: InstanceType<typeof ValidationObserver>,
    confirmEmailForm: InstanceType<typeof ValidationObserver>
  }

  timer: any = null
  time: number = 60
  step: number = 1
  email: string = ''
  code: string = ''

  async doneRequestCode (
    { data: { requestCode: { success, errors } } }: { data: RequestCodeMutation }
  ): Promise<void> {
    if (success) {
      this.step = 2
      this.timer = setInterval(() => { --this.time }, 1000)
      this.time = 60
    } else {
      await this.$refs.requestCodeForm.setErrors(errors.reduce(
        (a: { [key: string]: string[] }, c: ErrorFieldType) => {
          return { ...a, [this.t(c.field)]: c.messages }
        }, {}))
    }
  }

  async doneConfirmEmail (
    { data: { confirmEmail: { success, errors, user } } } : { data: ConfirmEmailMutation }
  ): Promise<void> {
    if (success) {
      await this.$store.dispatch('auth/changeVerification', user)
      this.step = 3
      setTimeout(() => {
        this.$router.push(this.localePath({ name: 'index' }))
      }, 2000)
    } else {
      await this.$refs.confirmEmailForm.setErrors(errors.reduce(
        (a: { [key: string]: string[] }, c: ErrorFieldType) => {
          return { ...a, [this.t(c.field)]: c.messages }
        }, {}))
    }
  }

  reRequestCode () {
    if (this.time > 0) {
      return
    }
    this.step = 1
    this.time = 60
    this.resetRequestCode()
  }

  resetRequestCode () {
    if (this.timer !== null) {
      clearInterval(this.timer)
      this.timer = null
    }
  }

  beforeDestroy () {
    this.resetRequestCode()
  }

  /**
   * Получение перевода относильно локального пути
   * @param path
   * @param values
   * @return
   */
  t (path: string, values: any = undefined): string {
    return this.$t(`user.verification.${path}`, values) as string
  }
}
</script>
