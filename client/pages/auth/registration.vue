<template lang="pug">
  bread-crumbs(:items="breadCrumbs")
    v-row
      v-col.mx-auto(v-if="!registered" lg="6" md="8" cols="12")
        apollo-mutation(
          v-slot="{ mutate, loading, error }"
          :mutation="require('~/gql/core/mutations/user/register.graphql')"
          :variables="{ username, email, lastName, firstName, sirName, birthday, password, agreement }"
          @done="onDone"
          tag
        )
          ValidationObserver(v-slot="{ handleSubmit, invalid }" ref="registerForm")
            form(@submit.prevent="handleSubmit(mutate)")
                v-card
                  v-card-title {{ t('register') }}
                  v-card-text
                    v-alert(v-if="error" type="error") {{ t('mutationBusinessLogicError', error) }}
                    //- Логин (номер зачетки) и Email
                    ValidationProvider(
                      :name="t('username')"
                      rules="required|min:2|max:50"
                      v-slot="{ errors, valid }"
                      tag="div"
                      )
                      v-text-field(
                        v-model="username"
                        :label="t('username')"
                        :error-messages="errors"
                        :success="valid"
                        autocomplete="of"
                        )
                    ValidationProvider(
                      :name="t('email')"
                      rules="required|email"
                      v-slot="{ errors, valid }"
                      tag="div"
                      )
                      v-text-field(
                        v-model="email"
                        :label="t('email')"
                        :error-messages="errors"
                        :success="valid"
                        autocomplete="of"
                        )
                    //- ФИО
                    ValidationProvider(
                      :name="t('lastName')"
                      rules="required|min:2|max:50"
                      v-slot="{ errors, valid }"
                      tag="div"
                      )
                      v-text-field(
                        v-model="lastName"
                        :label="t('lastName')"
                        :error-messages="errors"
                        :success="valid"
                        autocomplete="of"
                        )
                    ValidationProvider(
                      :name="t('firstName')"
                      rules="required|min:2|max:50"
                      v-slot="{ errors, valid }"
                      tag="div"
                      )
                      v-text-field(
                        v-model="firstName"
                        :label="t('firstName')"
                        :error-messages="errors"
                        :success="valid"
                        autocomplete="of"
                        )
                    ValidationProvider(
                      :name="t('sirName')"
                      rules="min:2|max:50"
                      v-slot="{ errors, valid }"
                      tag="div"
                      )
                      v-text-field(
                        v-model="sirName"
                        :label="t('sirName')"
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
                        ValidationProvider(
                          :name="t('birthday')"
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
                            :label="t('birthday')"
                            readonly)
                      v-date-picker(v-model="birthday" @input="birthdayMenu = false")
                    //- Пароль
                    ValidationProvider(
                      :name="t('password')"
                      rules="required|min:8|confirmed:confirmation"
                      v-slot="{ errors, valid }"
                      tag="div"
                      )
                      v-text-field(
                        v-model="password"
                        :label="t('password')"
                        type="password"
                        :error-messages="errors"
                        :success="valid"
                        autocomplete="of"
                        )
                    ValidationProvider(
                      :name="t('passwordConfirm')"
                      rules="required|min:8" v-slot="{ errors, valid }"
                      vid="confirmation"
                      tag="div"
                      )
                      v-text-field(
                        v-model="passwordConfirm"
                        :label="t('passwordConfirm')"
                        type="password"
                        :error-messages="errors"
                        :success="valid"
                        autocomplete="of"
                        )
                    //- Согласие на обработку персональных данных
                    ValidationProvider(
                      :name="t('agreement')"
                      rules="agreement"
                      v-slot="{ errors, valid}"
                      tag="div"
                      )
                      v-checkbox(
                        v-model="agreement"
                        :error-messages="errors"
                        :success="valid"
                        :label="t('agreement')"
                        )
                  v-card-actions.justify-center
                    v-btn(
                      type="submit"
                      :disabled="invalid"
                      color="success"
                      :loading="loading"
                      ) {{ $t('auth.doRegister') }}
                  v-card-text {{ $t('auth.registrationOption') }}
      v-col.mx-auto(v-else lg="6" md="8" cols="12")
        v-card
          v-card-title {{ $t('auth.successRegister') }}
          v-card-text.text-center
            v-icon(color="success" size="200") mdi-check-circle-outline
          v-card-actions
            v-btn.ma-auto(:to="localePath({ name: 'auth-login' })" color="success") {{ t('goToLoginPage') }}

</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'
import { MetaInfo } from 'vue-meta'
import { ValidationObserver } from 'vee-validate'
import { BreadCrumbsItem } from '~/types/devind'
import { ErrorFieldType, RegisterMutationPayload } from '~/types/graphql'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'

@Component<AuthRegistration>({
  name: 'AuthRegistration',
  middleware: 'guest',
  components: { BreadCrumbs },
  computed: {
    breadCrumbs (): BreadCrumbsItem [] {
      return [
        { text: this.t('register'), to: this.localePath({ name: 'auth-registration' }), exact: true }
      ]
    }
  },
  head (): MetaInfo {
    return { title: this.t('register') } as MetaInfo
  }
})
export default class AuthRegistration extends Vue {
  readonly breadCrumbs!: BreadCrumbsItem[]
  $refs!: {
    registerForm: InstanceType<typeof ValidationObserver>
  }

  email: string = ''
  username: string = ''
  lastName: string = ''
  firstName: string = ''
  sirName: string = ''
  birthday: string = ''
  password: string = ''
  passwordConfirm: string = ''
  agreement: boolean = true

  registered: boolean = false
  birthdayMenu: boolean = false

  onDone ({ data: { register } }: { data: { register: RegisterMutationPayload } }) {
    if (register.success) {
      this.registered = true
    } else {
      this.$refs.registerForm.setErrors(register.errors.reduce(
        (a: { [key: string]: string[] }, c: ErrorFieldType) => {
          return { ...a, [this.$t(`auth.registration.${this.$snakeToCamel(c.field)}`) as string]: c.messages }
        }, {}))
    }
  }

  /**
   * Получение перевода относильно локального пути
   * @param path
   * @param values
   * @return
   */
  t (path: string, values: any = undefined): string {
    return this.$t(`auth.registration.${path}`, values) as string
  }
}
</script>
