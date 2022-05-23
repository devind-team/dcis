export default {
  home: 'Проекты сборов',
  grid: {
    version: 'Версия: {version}',
    toolbar: {
      addRow: 'Добавить строку'
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
    cellText: {
      title: 'Изменение текста'
    },
    cellFiles: {
      title: 'Изменение файлов',
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
      delete: '@:delete',
      save: '@:save',
      deleteItemName: 'период'
    },
    addPeriod: {
      header: 'Добавление периода',
      name: 'Название периода',
      file: 'Файл с формой сбора',
      buttonText: 'Добавить период'
    },
    statuses: {
      open: 'Открыто',
      close: 'Закрыто',
      preparation: 'Подготовка'
    },
    delete: 'Удаление периода',
    deleteWarning: 'Период нельзя восстановить.'
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
