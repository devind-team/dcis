<template lang="pug">
v-footer(padless)
  v-container
    v-row
      v-col
        v-list(style="background: inherit;" dense)
          v-list-item(v-for="localLink in localLinks" :key="localLink.icon" :href="localLink.href")
            v-list-item-icon
              v-icon {{ localLink.icon }}
            v-list-item-content {{ localLink.text }}
          theme-color(v-slot="{ on }")
            v-list-item(v-on="on")
              v-list-item-icon
                v-icon mdi-theme-light-dark
              v-list-item-content {{ $t('index.theme.change') }}
      v-col(cols="4")
        v-list(style="background: inherit;" dense)
          v-list-item(v-for="foreignLink in foreignLinks" :key="foreignLink.icon" :href="foreignLink.href")
            v-list-item-icon
              v-icon {{ foreignLink.icon }}
            v-list-item-content {{ foreignLink.text }}
    v-divider.mb-3
    v-row
      v-col
        .caption.mt-auto {{ develop }}
      v-col(cols="4")
        ul.caption.text-right(style="list-style-type: none") {{ phones }}
          li +7(495) 225-14-43
          li +7(795) 225-14-47
  v-btn(v-show="upVisible" @click="$vuetify.goTo(0)" size="small" fab fixed bottom right color="primary")
    v-icon mdi-chevron-up
</template>

<script lang="ts">
import { useScroll } from '@vueuse/core'
import type { Ref } from '#app'
import { defineComponent, ref, onMounted, watchEffect } from '#app'
import ThemeColor from '~/components/global/ThemeColor.vue'

type ForeignLinksType = { text: string, href: string, icon: string }

export default defineComponent({
  components: { ThemeColor },
  setup () {
    const upVisible: Ref<boolean> = ref<boolean>(false)

    const develop: string = 'Разработка и сопровождение - ' +
      'Центр отраслевых информационно-аналитических систем "Национального исследовательского университета "МЭИ"'
    const phones: string = 'Многоканальные телефоны службы поддержки:'
    const localLinks: ForeignLinksType[] = [
      { text: 'Главная', href: '/', icon: 'mdi-home' },
      { text: 'Руководство пользователя', href: '/instructions/Инструкция.docx', icon: 'mdi-file' }
    ]
    const foreignLinks: ForeignLinksType[] = [
      { text: 'Личный кабинет', href: 'https://www.cbias.ru/sso_app/', icon: 'mdi-account-lock' },
      { text: 'Служба поддержки', href: 'https://www.cbias.ru/sso_app/support.spf', icon: 'mdi-chat-processing' },
      { text: 'Часто задаваемые вопросы', href: 'https://www.cbias.ru/faq/', icon: 'mdi-frequently-asked-questions' }
    ]

    onMounted(() => {
      const { y } = useScroll(document, { throttle: 500 })
      watchEffect(() => {
        upVisible.value = y.value > 200
      })
    })

    return { upVisible, develop, phones, localLinks, foreignLinks }
  }
})
</script>
