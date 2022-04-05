export default {
  home: 'Проекты сборов',
  grid: {
    toolbar: {
      addRow: 'Добавить строку'
    }
  },
  projects: {
    addProject: {
      header: 'Добавление проекта',
      name: 'Название проекта',
      short: 'Сокращенное название проекта',
      description: 'Описание проекта',
      visibility: 'Видимость',
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
    delete: 'Удаление периода',
    deleteWarning: 'Период нельзя восстановить.'
  },
  cellKinds: {
    n: 'Числовой',
    s: 'Строковый',
    text: 'Текст',
    money: 'Деньги',
    department: 'Департаменты'
  },
  documents: {
    add: {
      header: 'Создать новый документ',
      comment: 'Комментарий',
      status: 'Статус'
    },
    status: {
      name: 'Статус документа',
      header: 'Назначение статуса',
      buttonText: '@:add',
      comment: 'Комментарий'
    },
    unloading: {
      name: 'Выгрузить документ',
      rowAddDate: 'Дата добавления строки',
      rowUpdateDate: 'Дата последних изменений в строке',
      divisionName: 'Название дивизиона',
      divisionHeader: 'Начальник дивизиона',
      user: 'Пользователь, добавивший строку',
      additional: 'Дополнительные колонки',
      unload: 'Выгрузить'
    }
  }
}
