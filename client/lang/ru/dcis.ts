export default {
  home: 'Проекты сборов',
  projects: {
    name: '@:dcis.home',
    tableHeaders: {
      name: '@:name',
      description: 'Описание',
      createdAt: 'Дата добавления'
    },
    links: {
      periods: 'Периоды',
      settings: '@:settings'
    },
    addProject: {
      buttonText: 'Добавить проект',
      header: 'Добавление проекта',
      name: 'Название проекта',
      short: 'Сокращенное название проекта',
      description: 'Описание проекта',
      visibility: 'Видимость',
      department: 'Департаменты',
      organization: 'Организации'
    },
    changeProject: {
      header: 'Настройки проекта',
      archive: 'Архивировать',
      save: '@:save'
    },
    deleteProject: {
      header: 'Удаление проекта',
      warning: 'Проект нельзя восстановить.',
      itemName: 'проект',
      delete: '@:delete'
    }
  },
  periods: {
    name: 'Периоды',
    tableHeaders: {
      name: '@:name',
      status: 'Статус',
      createdAt: 'Дата добавления'
    },
    links: {
      documents: 'Документы',
      divisions: 'Дивизионы',
      groups: 'Группы',
      users: 'Пользователи',
      sheets: 'Таблица',
      settings: '@:settings'
    },
    statuses: {
      preparation: 'Подготовка',
      open: 'Открыто',
      close: 'Закрыто'
    },
    addPeriod: {
      buttonText: 'Добавить период',
      header: 'Добавление периода',
      name: 'Название периода',
      file: 'Файл с формой сбора',
      multiple: 'Множественное заполнение'
    },
    changePeriod: {
      header: 'Настройки периода',
      name: 'Название периода',
      status: 'Статус проекта',
      start: 'Дата начала периода',
      expiration: 'Дата окончания периода',
      multiple: 'Множественное заполнение',
      privately: 'Приватность полей',
      save: '@:save'
    },
    deletePeriod: {
      header: 'Удаление периода',
      warning: 'Период нельзя восстановить.',
      itemName: 'период',
      delete: '@:delete'
    },
    divisions: {
      name: '@:dcis.periods.links.divisions',
      addDivisions: {
        buttonText: 'Добавить дивизионы',
        header: 'Добавление дивизионов',
        name: '@:name'
      },
      tableHeaders: {
        name: '@:name',
        actions: '@:actions'
      },
      deleteDivision: {
        tooltip: '@:delete',
        itemName: 'дивизион'
      }
    },
    groups: {
      name: '@:dcis.periods.links.groups',
      addGroup: {
        buttonText: 'Добавить группу',
        header: 'Добавление группы',
        name: 'Название группы'
      },
      copyGroups: {
        buttonText: 'Импортировать группы',
        header: 'Импорт групп из другого периода',
        period: 'Период',
        groups: 'Группы'
      },
      deleteGroup: {
        tooltip: '@:delete',
        itemName: 'группу'
      },
      changePrivileges: {
        buttonText: 'Изменить привилегии',
        tableHeaders: {
          name: 'Название привилегии',
          key: 'Ключ'
        }
      }
    },
    users: {
      name: '@:dcis.periods.links.users',
      tableHeaders: {
        avatar: 'Аватар',
        fullname: 'ФИО',
        username: 'Логин',
        email: 'Email',
        actions: 'Действия'
      },
      addUser: {
        buttonText: 'Добавить пользователя',
        header: 'Добавление пользователя',
        user: 'Пользователь',
        groups: 'Группы',
        privileges: 'Привилегии',
        userExistWarning: 'Пользователь уже состоит в периоде'
      },
      changeGroups: {
        buttonText: 'Изменить группы',
        header: 'Изменение групп пользователя',
        tooltip: '@:dcis.periods.users.changeGroups.buttonText',
        tableHeaders: {
          name: 'Название группы'
        }
      },
      changePrivileges: {
        buttonText: 'Изменить привилегии',
        header: 'Изменение привилегий пользователя',
        tooltip: '@:dcis.periods.users.changePrivileges.buttonText',
        tableHeaders: {
          name: 'Название привилегии'
        }
      }
    },
    sheets: {
      name: '@:dcis.periods.links.sheets'
    }
  },
  documents: {
    name: 'Документы',
    version: 'Версия {version}',
    tableHeaders: {
      version: 'Версия',
      comment: 'Комментарий',
      createdAt: 'Дата добавления',
      lastStatus: 'Статус'
    },
    tableItems: {
      version: '@:dcis.documents.version',
      statusAssigned: 'Назначен: {assigned}'
    },
    addDocument: {
      buttonText: 'Добавить документ',
      header: 'Добавление документа',
      comment: 'Комментарий',
      status: 'Статус',
      lastDocument: 'Значения из документа',
      version: '@:dcis.documents.version'
    },
    status: {
      header: 'Добавление статуса',
      subheader: '@:dcis.documents.version',
      status: 'Статус',
      comment: 'Комментарий',
      buttonText: '@:add'
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
  },
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
  }
}
