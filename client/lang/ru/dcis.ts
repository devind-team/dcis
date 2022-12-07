export default {
  home: 'Проекты сборов',
  projects: {
    name: '@:dcis.home',
    divisions: 'Мои организации',
    filter: {
      title: 'Фильтр проектов',
      active: 'Активные проекты',
      archive: 'Проекты в архиве',
      hidden: 'Скрытые проекты',
      noFiltrationMessage: 'Фильтры не заданы'
    },
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
    choicePeriod: 'Выбрать период',
    file: 'Выберете файл',
    tableHeaders: {
      name: '@:name',
      status: 'Статус',
      createdAt: 'Дата добавления'
    },
    links: {
      documents: 'Документы',
      monitoring: 'Мониторинг',
      departments: 'Департаменты',
      organizations: 'Организации',
      groups: 'Группы',
      users: 'Пользователи',
      limitations: 'Ограничения',
      attributes: 'Атрибуты',
      sheets: 'Таблица',
      report: 'Сводный отчет',
      settings: '@:settings'
    },
    statuses: {
      preparation: 'Подготовка',
      open: 'Открыто',
      close: 'Закрыто'
    },
    addDivisions: {
      file: 'Выберете файл'
    },
    addPeriod: {
      buttonText: 'Добавить период',
      header: 'Добавление периода',
      name: 'Название периода',
      xlsxFile: 'Файл с формами сбора',
      limitationsFile: 'Ограничения, накладываемые на формы',
      downloadTemplate: 'Скачать шаблон файла',
      readonlyFillColor: 'Запретить редактирование ячеек с заливкой',
      multiple: 'Множественное заполнение',
      versioning: 'Разрешить множество версий'
    },
    changePeriod: {
      header: 'Настройки периода',
      name: 'Название периода',
      status: 'Статус периода',
      start: 'Дата начала периода',
      expiration: 'Дата окончания периода',
      multiple: 'Множественное заполнение',
      privately: 'Приватность полей',
      versioning: 'Разрешить множество версий',
      save: '@:save'
    },
    deletePeriod: {
      header: 'Удаление периода',
      warning: 'Период нельзя восстановить.',
      itemName: 'период',
      delete: '@:delete'
    },
    divisions: {
      departmentsName: '@:dcis.periods.links.departments',
      organizationsName: '@:dcis.periods.links.organizations',
      addDivisions: {
        departmentsButtonText: 'Добавить департаменты',
        organizationsButtonText: 'Добавить организации',
        departmentsHeader: 'Добавление департаментов',
        organizationsHeader: 'Добавление организаций',
        name: '@:name'
      },
      tableHeaders: {
        name: '@:name',
        actions: '@:actions'
      },
      deleteDivision: {
        tooltip: '@:delete',
        departmentItemName: 'департамент',
        organizationItemName: 'организацию'
      }
    },
    limitations: {
      name: '@:dcis.periods.links.limitations',
      changeMenu: {
        buttonText: 'Изменить ограничения',
        updateLimitationFromFile: {
          buttonText: 'Обновить ограничения из файла',
          header: 'Обновление ограничения из файла',
          limitationsFile: 'Файл с новыми ограничениями',
          downloadTemplate: 'Скачать шаблон файла'
        },
        addLimitation: {
          buttonText: 'Добавить ограничение',
          header: 'Добавление ограничения',
          formula: 'Формула ограничения',
          errorMessage: 'Сообщение об ошибке',
          sheet: 'Форма'
        }
      },
      tableHeaders: {
        sheet: 'Форма',
        formula: 'Формула',
        errorMessage: 'Сообщение об ошибке',
        actions: '@:actions'
      },
      tooltips: {
        delete: '@:delete',
        change: '@:change'
      },
      changeLimitation: {
        header: 'Изменение ограничения',
        buttonText: 'Изменить ограничение',
        formula: 'Формула ограничения',
        errorMessage: 'Сообщение об ошибке',
        sheet: 'Форма'
      },
      deleteItemName: 'ограничение'
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
    },
    report: {
      name: '@:dcis.periods.links.report',
      settings: {
        unload: 'Выгрузить сводный отчет'
      },
      documentsFilter: {
        title: 'Выбор документов',
        noFiltrationMessage: 'Выбрать документы',
        multipleMessage: 'Выбрано документов: {count}',
        selectMainDocument: 'Выбрать основной документ',
        mainDocumentSelection: 'Выбор основного документа',
        mainDocument: 'Выбран основной документ: {divisionId}',
        propertiesForm: {
          header: 'Изменение свойств отображения документа',
          subheader: 'Документ: {divisionId}',
          isVisible: 'Отображать дочерние строки',
          color: 'Выделять цветом',
          buttonText: 'Изменить свойства'
        },
        aggregationFilter: {
          title: 'Выбор метода агрегации',
          selectAggregation: 'Выбрать метод агрегации',
          aggregation: 'Выбран метод агрегации: {method}',
          concat: 'Сцепление строк',
          sum: 'Сумма',
          avg: 'Среднее арифметическое',
          max: 'Максимальное значение',
          min: 'Минимальное значение'
        }
      },
      rowsFilter: {
        title: 'Выбор расширенных строки',
        noFiltrationMessage: 'Выбрать расширенные строки',
        multipleMessage: 'Выбрано расширенных строк: {count}'
      }
    }
  },
  documents: {
    name: 'Документы',
    version: 'Версия {version}',
    divisionFilterOrganization: {
      title: 'Фильтр организаций',
      noFiltrationMessage: 'Все организации',
      multipleMessage: '{name} и еще {restLength} организаций | {name} и еще {restLength} организация |' +
        ' {name} и еще {restLength} организации'
    },
    divisionFilterDepartment: {
      title: 'Фильтр департаментов',
      noFiltrationMessage: 'Все департаменты',
      multipleMessage: '{name} и еще {restLength} департаментов | {name} и еще {restLength} департамент |' +
        ' {name} и еще {restLength} департамента'
    },
    statusFilter: {
      title: 'Фильтр статусов',
      noFiltrationMessage: 'Все статусы',
      multipleMessage: '{name} и еще {restLength} статусов | {name} и еще {restLength} статус |' +
        ' {name} и еще {restLength} статуса'
    },
    tableHeaders: {
      version: 'Версия',
      comment: 'Комментарий',
      createdAt: 'Дата добавления',
      updatedAt: 'Дата последнего изменения',
      organization: '@:dcis.documents.addDocument.organization',
      department: '@:dcis.documents.addDocument.department',
      lastStatus: 'Статус'
    },
    tableItems: {
      version: '@:dcis.documents.version',
      statusAssigned: 'Назначен: {assigned}'
    },
    addDocument: {
      buttonText: 'Добавить документ',
      formText: 'Добавить новый документ',
      header: 'Добавление документа',
      comment: 'Комментарий',
      status: 'Статус',
      department: 'Департамент',
      organization: 'Организация',
      lastDocument: 'Значения из документа',
      version: '@:dcis.documents.version'
    },
    addDocumentData: {
      buttonText: 'Загрузить данные',
      header: 'Импорт документов',
      file: 'Выберете файл',
      status: '@:dcis.documents.addDocument.status',
      comment: '@:dcis.documents.addDocument.comment'
    },
    status: {
      header: 'Изменение статусов',
      readonlyHeader: 'Статусы',
      subheader: '@:dcis.documents.version',
      tableErrorsMessage: 'Возникли ошибки в ограничениях',
      tableErrorsTitle: 'Ошибки в ограничениях',
      status: 'Статус',
      comment: 'Комментарий',
      buttonText: '@:add',
      delete: {
        itemName: 'статус',
        tooltip: '@:delete'
      }
    },
    unloadDocument: {
      name: 'Выгрузить документ',
      additional: 'Дополнительные колонки',
      rowAddDate: 'Дата добавления строки',
      rowUpdateDate: 'Дата последних изменений в строке',
      departmentName: 'Название департамента',
      organizationName: 'Название организации',
      departmentHead: 'Начальник департамента',
      organizationHead: 'Начальник организации',
      user: 'Пользователь, добавивший строку',
      unload: 'Выгрузить'
    },
    tabs: {
      tabNameDocuments: {
        name: 'Документы'
      },
      tabNameNotSupplied: {
        name: 'Не подавшие'
      }
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
      f: 'Формула',
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
      readonly: 'Только для чтения',
      fix: 'Закрепление столбцов/строк',
      fontSize: 'Шрифт',
      kind: 'Тип',
      commaDecrease: 'Уменьшить разрядность',
      commaIncrease: 'Увеличить разрядность',
      aggregation: 'Агрегация ячеек',
      aggregationTitle: 'Настройки агрегации',
      aggregationChoice: 'Метод агрегации',
      aggregationDefault: 'Значение по умолчанию: {value}',
      aggregationKind: {
        empty: 'Не задано',
        sum: 'Сумма',
        avg: 'Среднее арифметическое',
        max: 'Максимальное значение',
        min: 'Минимальное значение'
      }
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
      hide: '@:hide',
      makeDynamic: 'Разрешить дочерние строки',
      buttonText: '@:save'
    },
    changeValue: 'Изменение значения',
    cellFiles: {
      readonlyHeader: 'Файлы',
      file: 'Файл №{number}',
      newFiles: 'Новые файлы',
      uploadArchive: 'Скачать архив'
    }
  },
  sheets: {
    settings: {
      show: 'Настройки вывода',
      name: 'Название листов',
      showHead: 'Отображать головным учреждениям',
      showChild: 'Отображать филиалам'
    }
  },
  attributes: {
    adds: 'Добавить атрибуты',
    add: 'Добавить атрибут',
    change: 'Изменить',
    delete: 'Удалить',
    addMenu: {
      header: 'Добавление атрибута',
      buttonText: 'Добавить',
      name: 'Наименование',
      placeholder: 'Подсказка',
      key: 'Ключ',
      kind: 'Тип',
      default: 'Значение по умолчанию',
      mutable: 'Разрешить изменение',
      text: 'Текст',
      bigmoney: 'Тысячи',
      bool: 'Переключатель',
      date: 'Дата',
      files: 'Файл',
      money: 'Рубли',
      numeric: 'Числовое значение',
      aggregation: 'Агрегация',
      all: 'Ошибка добавления'
    },
    changeMenu: {
      header: 'Изменение атрибута',
      buttonText: 'Изменить',
      name: 'Наименование',
      placeholder: 'Подсказка',
      key: 'Ключ',
      kind: 'Тип',
      default: 'Значение по умолчанию',
      mutable: 'Разрешить изменение'
    },
    tableHeaders: {
      name: 'Название параметра',
      key: 'Ключ',
      default: 'По умолчанию',
      placeholder: 'Подсказка',
      action: 'Действие'
    }
  }
}
