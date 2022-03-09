export default {
  index: 'Панель управления',
  support: 'Поддержка',
  groups: 'Группы пользователей',
  permissionFrom: 'Привилегии из группы',
  permissions: 'Привилегии пользователей',
  usersFile: 'Файл с пользователями',
  dictionaries: 'Справочники',
  dictionary: { profile: 'Профиль' },
  ac: {
    name: 'Администрирование',
    activity: {
      record: 'Запись',
      shownOf: '@:shownOf',
      loadMore: '@:loadMore',
      tableHeaders: {
        user: 'Пользователь',
        action: 'Действие',
        contentType: 'Модель',
        objectId: 'Объект',
        session: 'Система',
        createdAt: 'Дата события',
        info: 'Информация'
      },
      actions: {
        deleted: 'удалена',
        created: 'создана',
        changed: 'изменена'
      }
    },
    groups: {
      name: 'Группы',
      change: '@:change',
      deleteGroup: 'Удалить группу',
      tagged: 'Отмечено {count} из {totalCount}',
      tableHeaders: {
        name: '@:name',
        contentType: 'Приложение/Модель',
        codename: 'Код привилегии'
      }
    },
    history: {
      shownOf: 'Показано записей {count} из {totalCount}',
      loadMore: '@:loadMore',
      tableHeaders: {
        user: 'Пользователь',
        page: 'Страница',
        browser: 'Браузер',
        device: 'Устройство',
        os: 'Операционная система',
        createdAt: 'Дата события',
        time: 'Время обработки'
      }
    },
    permissions: {
      name: 'Привилегии',
      shownOf: 'Показано записей {count}',
      tableHeaders: {
        name: '@:name',
        contentType: 'Приложение/Модель',
        codename: 'Код привилегии'
      }
    },
    users: {
      name: 'Пользователи',
      addUsers: 'Добавить пользователей',
      shownOf: '@:shownOf',
      unloadUsers: 'Выгрузить пользователей',
      search: '@:search',
      change: '@:change',
      tableHeaders: {
        avatar: 'Аватар',
        name: 'ФИО',
        username: 'Логин',
        email: 'Email',
        groups: 'Группы',
        createdAt: 'Регистрация'
      },
      changeGroups: {
        header: 'Изменить группы',
        buttonText: '@:change',
        noGroups: 'Не выбраны'
      }
    }
  }
}
