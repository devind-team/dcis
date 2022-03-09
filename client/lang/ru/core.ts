export default {
  filters: {
    usersFilter: {
      title: 'Фильтр пользователей',
      noFiltrationMessage: 'Все пользователи',
      multipleMessage: '{name} и еще {restLength} пользователей | {name} и еще {restLength} пользователь |' +
          ' {name} и еще {restLength} пользователь'
    }
  },
  settings: {
    steps: {
      user: 'Настройки пользователя',
      app: 'Настройки приложения',
      language: 'Добавление языков'
    },
    continue: 'Продолжить',
    back: 'Назад',
    complete: 'Завершить',
    keys: {
      APP_NAME: 'Название приложения',
      URL: 'URL',
      API_URL: 'API URL',
      API_URL_BROWSER: 'API URL в браузере',
      WS_URL: 'WebSocket URL',
      CLIENT_ID: 'ID приложения',
      TINYMCE_API: 'TinyMCE API',
      ASK: 'Application server key'
    }
  }
}
