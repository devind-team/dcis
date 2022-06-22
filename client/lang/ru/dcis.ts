export default {
  home: 'Проекты сборов',
  grid: {
    version: 'Версия: {version}',
    sheet: {
      rename: 'Переименовать'
    },
    cellKinds: {
      n: 'Числовой',
      s: 'Строковый',
      text: 'Текст',
      fl: 'Файл',
      money: 'Деньги',
      department: 'Департаменты',
      classification: 'КБК'
    },
    toolbar: {
      addRow: 'Добавить строку'
    },
    sheetToolbar: {
      fontSize: 'Шрифт',
      kind: 'Тип'
    },
    columnWidth: 'Ширина: ',
    rowHeight: 'Высота: ',
    columnControl: {
      properties: '@:properties'
    },
    columnSettings: {
      header: 'Изменение свойств',
      subheader: 'Дата изменения: {updatedAt}',
      width: 'Ширина',
      fix: '@:fix',
      hide: '@:hide',
      kind: 'Тип ячейки по умолчанию',
      buttonText: '@:save'
    },
    rowControl: {
      properties: '@:properties',
      addRowAbove: 'Добавить строку выше',
      addRowBelow: 'Добавить строку ниже',
      addChildRow: 'Добавить дочернюю строку',
      deleteRow: 'Удалить строку'
    },
    rowSettings: {
      header: 'Изменение свойств',
      subheader: 'Дата изменения: {updatedAt}',
      height: 'Высота',
      fix: '@:fix',
      hide: '@:hide',
      makeDynamic: 'Разрешить дочерние строки',
      buttonText: '@:save'
    },
    changeValue: 'Изменение значения',
    cellFiles: {
      file: 'Файл №{number}',
      newFiles: 'Новые файлы',
      uploadArchive: 'Скачать архив'
    }
  },
  projects: {
    addProject: {
      header: 'Добавление проекта',
      name: 'Название проекта',
      short: 'Сокращенное название проекта',
      description: 'Описание проекта',
      visibility: 'Видимость',
      department: 'Департаменты',
      organization: 'Организации',
      buttonText: 'Добавить проект'
    },
    changeProject: {
      header: 'Настройки проекта',
      archive: 'Архивировать',
      delete: '@:delete',
      save: '@:save',
      deleteItemName: 'проект',
      warning: 'Проект нельзя восстановить.'
    }
  },
  periods: {
    header: 'Настройки периода',
    name: 'Наименование периода',
    status: 'Статус проекта',
    multiple: 'Множественное заполнение',
    privately: 'Приватность полей',
    start: 'Дата начала периода',
    expiration: 'Дата окончания периода',
    deleteItemName: 'период',
    actions: {
      addGroup: 'Добавить группу',
      delete: '@:delete',
      deleteGroup: 'Удалить группу',
      copyGroups: 'Копировать из сбора',
      save: '@:save',
      deleteItemName: 'период'
    },
    addPeriod: {
      header: 'Добавление периода',
      name: 'Название периода',
      file: 'Файл с формой сбора',
      multiple: 'Множественное заполнение',
      buttonText: 'Добавить период'
    },
    addPeriodGroup: {
      header: 'Добавление группы периода',
      name: 'Название группы периода',
      groups: 'Пользователи и привилегии из другой группы',
      buttonText: '@:add'
    },
    copyPeriodGroups: {
      header: 'Импорт групп из сбора',
      name: 'Название группы периода',
      groups: 'Группы',
      period: 'Период',
      buttonText: '@:add'
    },
    changePeriodUsers: {
      header: 'Добавление пользователей',
      buttonText: '@:add',
      addUsers: 'Добавить пользователей',
      avatar: 'Аватар',
      name: 'ФИО',
      users: 'Пользователи',
      jobPost: 'Должность',
      division: 'Объект сбора'
    },
    changePrivileges: {
      groupHeader: 'Изменениe привилегий',
      userHeader: 'Добавление привилегий пользователю',
      buttonChangeText: '@:change',
      buttonAddText: '@:add',
      change: 'Изменить привилегии',
      add: 'Добавить привилегии',
      deleteUser: 'Удалить из группы',
      name: 'Описание привилегии',
      privileges: 'Привилегии пользователя',
      key: 'Ключ',
      createdAt: 'Дата создания',
      alert: 'Не заданы привилегии сбора или группы'
    },
    divisions: {
      change: 'Изменить дивизионы',
      header: 'Настройка дивизионов',
      add: 'Добавить дивизионы',
      id: 'Идентификатор',
      action: 'Действия',
      formHeader: 'Изменение дивизионов',
      buttonText: '@:add',
      name: 'Название объекта',
      createdAt: 'Дата создания',
      shownOf: 'Показано записей:'
    },
    statuses: {
      open: 'Открыто',
      close: 'Закрыто',
      preparation: 'Подготовка'
    },
    delete: 'Удаление периода',
    deleteWarning: 'Период нельзя восстановить.'
  },
  documents: {
    add: {
      header: 'Создать новый документ',
      comment: 'Комментарий',
      status: 'Статус',
      lastDocument: 'Значения из документа'
    },
    status: {
      name: 'Статус документа',
      header: 'Назначение статуса',
      buttonText: '@:add',
      comment: 'Комментарий'
    },
    unloading: {
      name: 'Выгрузить документ',
      row_add_date: 'Дата добавления строки',
      row_update_date: 'Дата последних изменений в строке',
      division_name: 'Название дивизиона',
      division_head: 'Начальник дивизиона',
      user: 'Пользователь, добавивший строку',
      additional: 'Дополнительные колонки',
      unload: 'Выгрузить'
    }
  }
}
