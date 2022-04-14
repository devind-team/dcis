import { detect } from 'detect-browser'

export default defineNuxtPlugin(() => {
  const browser = detect()
  if (browser && browser.name === 'firefox') {
    document.body.classList.add('browser-firefox')
  } else {
    document.body.classList.add('browser-default')
  }
})
