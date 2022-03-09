<template lang="pug">
  v-btn(@click="subscribe" outlined color="success") {{ t('subscribe') }}
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend<any, any, any, any>({
  methods: {
    subscribe () {
      Notification.requestPermission((status) => {
        if (status === 'granted' && 'serviceWorker' in navigator) {
          navigator.serviceWorker.getRegistration().then((reg) => {
            const options = {
              body: this.t('studentSent'),
              icon: 'icon.png',
              vibrate: [100, 50, 100],
              data: { primaryKey: 1 },
              actions: [
                { action: 'explore', title: this.t('explore') },
                { action: 'close', title: this.t('close') }
              ]
            }
            reg!.showNotification(this.t('newLaboratoryWork'), options)
            reg!.pushManager.getSubscription().then((sub) => {
              if (sub === null) {
                reg!.pushManager.subscribe({
                  userVisibleOnly: true,
                  applicationServerKey: this.urlBase64ToUint8Array(this.$nuxt.$config.ASK)
                }).then((sub: PushSubscription | null) => {
                  if (sub instanceof PushSubscription) {
                    // const browser: { name: string, version: string } = this.loadVersionBrowser(window.navigator.userAgent)
                    // const endpointParts = sub!.endpoint.split('/')
                    // const data = {
                    //   endpoint: sub.endpoint,
                    //   // @ts-ignore
                    //   p256dh: btoa(String.fromCharCode.apply(null, new Uint8Array(sub.getKey('p256dh')))),
                    //   // @ts-ignore
                    //   auth: btoa(String.fromCharCode.apply(null, new Uint8Array(sub.getKey('auth')))),
                    //   registrationId: endpointParts[endpointParts.length - 1],
                    //   browser: browser.name.toUpperCase()
                    // }
                    // console.log(data) // send data to server
                  }
                })
              } else {
                // you have subscription, update the database on your server
              }
            })
          })
        }
      })
    },
    urlBase64ToUint8Array (base64String: string): Uint8Array {
      const padding = '='.repeat((4 - base64String.length % 4) % 4)
      const base64 = (base64String + padding)
        .replace(/-/g, '+')
        .replace(/_/g, '/')

      const rawData = window.atob(base64)
      const outputArray = new Uint8Array(rawData.length)

      for (let i = 0; i < rawData.length; ++i) {
        outputArray[i] = rawData.charCodeAt(i)
      }
      return outputArray
    },
    loadVersionBrowser (userAgent: string): { name: string, version: string } {
      const ua: string = userAgent
      let m = ua.match(/(opera|chrome|safari|firefox|msie|trident(?=\/))\/?\s*(\d+)/i) || []
      if (/trident/i.test(m[1])) {
        const tem: never[] | RegExpExecArray = /\brv[ :]+(\d+)/g.exec(ua) || []
        return { name: 'IE', version: (tem[1] || '') }
      }
      if (m[1] === 'Chrome') {
        const tem: RegExpMatchArray | null = ua.match(/\bOPR\/(\d+)/)
        if (tem != null) {
          return { name: 'Opera', version: tem[1] }
        }
      }
      m = m[2] ? [m[1], m[2]] : [navigator.appName, navigator.appVersion, '-?']
      let tem
      if ((tem = ua.match(/version\/(\d+)/i)) != null) {
        m.splice(1, 1, tem[1])
      }
      return { name: m[0], version: m[1] }
    },
    /**
     * Получение перевода относильно локального пути
     * @param path
     * @param values
     * @return
     */
    t (path: string, values: any = undefined): string {
      return this.$t(`global.subscription.${path}`, values) as string
    }
  }
})
</script>
