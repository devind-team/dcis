import { Plugin, Context } from '@nuxt/types'

export default <Plugin> function ({ app: { i18n } }: Context) {
  i18n.pluralizationRules = {
    ru (choice: number) {
      if (choice === 0 || ((choice >= 5) && (choice <= 20))) {
        return 0
      }
      if (choice === 1) {
        return 1
      }
      if (choice >= 2 && choice <= 4) {
        return 2
      }
      const digits: number[] = String(choice).split('').map((strDigit: string) => Number(strDigit))
      const lastDigit: number = digits[digits.length - 1]
      if (lastDigit === 0 || lastDigit >= 5) {
        return 0
      }
      if (lastDigit === 1) {
        return 1
      }
      return 2
    }
  }
}
