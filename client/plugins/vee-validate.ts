import Vue from 'vue'
import { ValidationObserver, ValidationProvider, extend } from 'vee-validate'
import * as rules from 'vee-validate/dist/rules'
// @ts-ignore
import ru from 'vee-validate/dist/locale/ru.json'
Vue.component('ValidationObserver', ValidationObserver)
Vue.component('ValidationProvider', ValidationProvider)

for (const [rule, validation] of Object.entries(rules)) {
  // @ts-ignore
  extend(rule, { ...validation, message: ru.messages[rule] })
}

extend('confirmPassword', {
  params: ['target'],
  validate (value: string, { target }: { target: string }) {
    return value === target
  },
  message: 'Значение не совпадает с полем "Введите новый пароль"'
})

extend('agreement', {
  validate (value: boolean) {
    return value
  },
  message: 'Необходимо дать согласие'
})

extend('rate', {
  validate (value: string): boolean {
    return Number(value) > 0 && Number(value) <= 1
  },
  message: 'Занятость находится в пределах от 0 до 1'
})
