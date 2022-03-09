<template lang="pug">
  v-footer(padless)
    v-container
      v-row
        v-col(cols="12" md="9")
          .body-2 Email:&nbsp;
            strong {{ $getSettingValue('APP_EMAIL') }}
        v-col(cols="12" md="3")
          v-list(width="280" style="background: inherit;" dense)
            theme-color(v-slot="{ on }")
              v-list-item(v-on="on")
                v-list-item-icon
                  v-icon mdi-theme-light-dark
                v-list-item-content
                  v-list-item-title {{ $t('index.theme.change') }}
      v-row
        v-col(cols="12" md="9")
          .body-2.gray-text &copy; {{ $t('index.rights') }}. {{ new Date().getFullYear() }}
    v-btn(v-show="upVisible$" @click="$vuetify.goTo(0)" size="small" fab fixed bottom right color="primary")
      v-icon mdi-chevron-up
</template>

<script lang="ts">
import Vue from 'vue'
import { fromEvent } from 'rxjs'
import { pluck, map, debounceTime, startWith } from 'rxjs/operators'
import ThemeColor from '~/components/global/ThemeColor.vue'

export default Vue.extend<any, any, any, any>({
  components: { ThemeColor },
  data: () => ({
    upVisible$: false,
    counterSrc: ''
  }),
  subscriptions () {
    const upVisible$ = fromEvent(document, 'scroll').pipe(
      pluck('target', 'documentElement'),
      debounceTime(100),
      map((target: any) => ({ top: target.scrollTop + window.innerHeight, height: target.offsetHeight })),
      map(({ top, height }) => (top + 800 > height)),
      startWith(false),
      map(() => window.scrollY > 20)
    )
    return { upVisible$ }
  },
  mounted () {
    const s = screen.colorDepth ? screen.colorDepth : screen.pixelDepth
    this.counterSrc = 'https://counter.yadro.ru/hit?t11.6;r' + encodeURIComponent(document.referrer) +
      (typeof screen === 'undefined' ? '' : ';s' + screen.width + '*' + screen.height + '*' + s) +
      ';u' + encodeURIComponent(document.URL) + ';h' +
      encodeURIComponent(document.title.substring(0, 150)) + ';' + Math.random() as string
  }
})
</script>
