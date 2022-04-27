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
    addPeriodGroup: {
      header: 'Добавление группы периода',
      name: 'Название группы периода',
      groups: 'Пользователи и привилегии из другой группы',
      buttonText: '@:add'
    },
    changePeriodUsers: {
      header: 'Добавление пользователей',
      buttonText: '@:add'
    },
    changePeriodGroupPrivileges: {
      header: 'Изменениe привилегий {groupName}',
      buttonText: '@:change'
    },
    privileges: {
      name: 'Описание привилегии',
      key: 'Ключ',
      createdAt: 'Дата создания'
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
