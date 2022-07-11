<template lang="pug">
bread-crumbs(:items="breadCrumbs")
  v-row
    v-col.mx-auto(v-if="!registered" lg="6" md="8" cols="12")
      v-alert(type="info") {{ $t('auth.registrationOption') }}
      mutation-form(
        @done="onDone"
        :mutation="require('~/gql/core/mutations/user/register.graphql')"
        :variables="{ username, email, lastName, firstName, sirName, birthday, password, agreement }"
        :header="String($t('auth.registration.register'))"
        :button-text="String($t('auth.doRegister'))"
         mutation-name="register"
         i18n-path="auth.registration"
      )
        template(#form)
          validation-provider(
            :name="String($t('auth.registration.username'))"
            rules="required|min:2|max:50"
            v-slot="{ errors, valid }"
            tag="div"
            )
            v-text-field(
              v-model="username"
              :label="$t('auth.registration.username')"
              :error-messages="errors"
              :success="valid"
              autocomplete="of"
              )
          validation-provider(
            :name="String($t('auth.registration.email'))"
            rules="required|email"
            v-slot="{ errors, valid }"
            tag="div"
            )
            v-text-field(
              v-model="email"
              :label="$t('auth.registration.email')"
              :error-messages="errors"
              :success="valid"
              autocomplete="of"
              )
          //- ФИО
          validation-provider(
            :name="String($t('auth.registration.lastName'))"
            rules="required|min:2|max:50"
            v-slot="{ errors, valid }"
            tag="div"
            )
            v-text-field(
              v-model="lastName"
              :label="$t('auth.registration.lastName')"
              :error-messages="errors"
              :success="valid"
              autocomplete="of"
              )
          validation-provider(
            :name="String($t('auth.registration.firstName'))"
            rules="required|min:2|max:50"
            v-slot="{ errors, valid }"
            tag="div"
            )
            v-text-field(
              v-model="firstName"
              :label="$t('auth.registration.firstName')"
              :error-messages="errors"
              :success="valid"
              autocomplete="of"
              )
          validation-provider(
            :name="String($t('auth.registration.sirName'))"
            rules="min:2|max:50"
            v-slot="{ errors, valid }"
            tag="div"
            )
            v-text-field(
              v-model="sirName"
              :label="$t('auth.registration.sirName')"
              :error-messages="errors"
              :success="valid"
              autocomplete="of"
            )
          //- Дата рождения
          v-menu(
            v-model="birthdayMenu"
            :close-on-content-click="false"
            bottom max-width="290px"
            transition="scale-transition"
            min-width="290px"
          )
            template(v-slot:activator="{ on }")
              validation-provider(
                :name="String($t('auth.registration.birthday'))"
                rules="required"
                v-slot="{ errors, valid }"
                tag="div"
              )
                v-text-field(
                  v-on="on"
                  v-model="birthday"
                  :error-messages="errors"
                  :success="valid"
                  prepend-icon="mdi-calendar"
                  :label="$t('auth.registration.birthday')"
                  readonly
                )
            v-date-picker(v-model="birthday" @input="birthdayMenu = false")
          //- Пароль
          validation-provider(
            :name="String($t('auth.registration.password'))"
            rules="required|min:8|confirmed:confirmation"
            v-slot="{ errors, valid }"
            tag="div"
          )
            v-text-field(
              v-model="password"
              :label="$t('auth.registration.password')"
              type="password"
              :error-messages="errors"
              :success="valid"
              autocomplete="of"
            )
          validation-provider(
            :name="String($t('auth.registration.passwordConfirm'))"
            rules="required|min:8" v-slot="{ errors, valid }"
            vid="confirmation"
            tag="div"
          )
            v-text-field(
              v-model="passwordConfirm"
              :label="$t('auth.registration.passwordConfirm')"
              type="password"
              :error-messages="errors"
              :success="valid"
              autocomplete="of"
            )
          //- Согласие на обработку персональных данных
          validation-provider(
            :name="String($t('auth.registration.agreement'))"
            rules="agreement"
            v-slot="{ errors, valid}"
            tag="div"
          )
            v-checkbox(
              v-model="agreement"
              :error-messages="errors"
              :success="valid"
              :label="$t('auth.registration.agreement')"
            )
    v-col.mx-auto(v-else lg="6" md="8" cols="12")
      v-card
        v-card-title {{ $t('auth.successRegister') }}
        v-card-text.text-center
          v-icon(color="success" size="200") mdi-check-circle-outline
        v-card-actions
          v-btn.ma-auto(:to="localePath({ name: 'auth-login' })" color="success") {{ $t('auth.registration.goToLoginPage') }}
</template>

<script lang="ts">
import { computed, defineComponent, ref, useNuxt2Meta } from '#app'
import { useI18n } from '~/composables'
import { BreadCrumbsItem } from '~/types/devind'
import { RegisterMutationPayload } from '~/types/graphql'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import MutationForm from '~/components/common/forms/MutationForm.vue'

export default defineComponent({
  components: { MutationForm, BreadCrumbs },
  middleware: 'guest',
  setup () {
    const { t, localePath } = useI18n()

    useNuxt2Meta({ title: t('auth.registration.register') as string })
    const breadCrumbs = computed<BreadCrumbsItem[]>(() => ([
      { text: t('auth.registration.register') as string, to: localePath({ name: 'auth-registration' }), exact: true }
    ]))

    const email = ref<string>('')
    const username = ref<string>('')
    const lastName = ref<string>('')
    const firstName = ref<string>('')
    const sirName = ref<string>('')
    const birthday = ref<string>('')
    const password = ref<string>('')
    const passwordConfirm = ref<string>('')
    const agreement = ref<boolean>(true)

    const registered = ref<boolean>(false)
    const birthdayMenu = ref<boolean>(false)

    const onDone = ({ data: { register } }: { data: { register: RegisterMutationPayload } }) => {
      if (!register.errors.length) {
        registered.value = true
      }
    }

    return {
      breadCrumbs,
      email,
      username,
      lastName,
      firstName,
      sirName,
      birthday,
      password,
      passwordConfirm,
      agreement,
      registered,
      birthdayMenu,
      onDone
    }
  }
})
</script>
