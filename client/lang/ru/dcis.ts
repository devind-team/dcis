export default {
  home: 'Проекты сборов',
  projects: {
    name: '@:dcis.home',
    divisions: 'Мои организации',
    filter: {
      title: 'Фильтр проектов',
      active: 'Активные проекты',
      hidden: 'Скрытые проекты',
      archive: 'Проекты в архиве',
      notArchive: 'Проекты не в архиве',
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
    archive: {
      name: 'Архив',
      document: 'Документ'
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
      unload: 'Выгрузка',
      support: 'Методическое обеспечение',
      settings: '@:settings',
      aggregations: 'Агрегация'
    },
    statuses: {
      preparation: 'Подготовка',
      open: 'Открыто',
      close: 'Закрыто'
    },
    statusFilter: {
      title: 'Фильтр статусов периода',
      noFiltrationMessage: 'Все статусы',
      multipleMessage: '{name} и еще {restLength} статусов | {name} и еще {restLength} статус |' +
        ' {name} и еще {restLength} статуса'
    },
    organizationFilter: {
      title: 'Фильтр организаций',
      noFiltrationMessage: 'Выбрать организации',
      multipleMessage: 'Выбрано организаций: {count}',
      tableHeaders: {
        id: 'Идентификатор',
        name: 'Название',
        kpp: 'Кбк',
        inn: 'ИНН',
        kodbuhg: 'Бухгалтерский код'
      },
      levelFilter: {
        title: 'Фильтр типа организации',
        noFiltrationMessage: 'Все типы',
        multipleMessage: '{name} и еще {restLength} типы | {name} и еще {restLength} тип |' +
          ' {name} и еще {restLength} типа',
        types: {
          head: 'Головное',
          branch: 'Филиал'
        }
      }
    },
    departmentFilter: {
      title: 'Фильтр департаментов',
      noFiltrationMessage: 'Выбрать департаменты',
      multipleMessage: 'Выбрано департаментов: {count}',
      tableHeaders: {
        id: 'Идентификатор',
        name: 'Название',
        code: 'Код департамента'
      }
    },
    organizationKindFilter: {
      title: 'Фильтр типов организаций',
      noFiltrationMessage: 'Выбрать типы организаций',
      multipleMessage: '{name} и еще {restLength} типов организаций | {name} и еще {restLength} тип организаций |' +
        ' {name} и еще {restLength} типа организаций'
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
        addLimitation: {
          buttonText: 'Добавить ограничение',
          header: 'Добавление ограничения',
          formula: 'Формула ограничения',
          errorMessage: 'Сообщение об ошибке',
          sheet: 'Форма'
        },
        updateLimitationFromFile: {
          buttonText: 'Обновить ограничения из файла',
          header: 'Обновление ограничения из файла',
          limitationsFile: 'Файл с новыми ограничениями',
          downloadTemplate: 'Скачать шаблон файла'
        },
        unloadLimitation: {
          content: 'Выгрузить ограничения'
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
    aggregationCells: {
      name: '@:dcis.periods.links.aggregations',
      kinds: {
        sum: 'Сумма',
        avg: 'Среднее арифметическое',
        max: 'Максимальное значение',
        min: 'Минимальное значение'
      },
      changeMenu: {
        buttonText: 'Изменить агрегацию',
        addAggregation: {
          buttonText: 'Добавить агрегацию',
          header: 'Добавление агрегацию',
          errorMessage: 'Сообщение об ошибке',
          cell: 'Ячейка',
          method: 'Метод агрегации',
          cells: 'Агрегируемые ячейки',
          sheet: 'Лист'
        },
        addCell: {
          buttonText: 'Добавить ячейку'
        },
        updateAggregationFromFile: {
          buttonText: 'Обновить агрегацию из файла',
          header: 'Обновление агрегацию из файла',
          aggregationsFile: 'Файл с новой агрегацией',
          downloadTemplate: 'Скачать шаблон файла'
        },
        unloadAggregation: {
          content: 'Выгрузить агрегацию'
        }
      },
      tableHeaders: {
        position: 'Ячейка',
        aggregateType: 'Метод агрегации',
        listAggregateCells: 'Агрегируемые ячейки',
        actions: '@:actions'
      },
      tooltips: {
        delete: '@:delete'
      },
      deleteItemName: 'агрегацию ячейки'
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
    methodicalSupport: {
      file: 'файл',
      shownOf: '@:shownOf',
      uploadFiles: 'Загрузить файлы',
      downloadFile: 'Скачать файл',
      changeName: 'Изменить название',
      deleteFile: 'Удалить файл',
      kB: 'кБ',
      tableHeaders: {
        name: '@:name',
        ext: 'Тип файла',
        updated: 'Загружен',
        size: 'Размер',
        actions: 'Действия'
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
      documentsFilter: {
        title: 'Выбор документов',
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
        title: 'Выбор расширенных строк'
      }
    },
    unload: {
      name: '@:dcis.periods.links.unload',
      organizationsFilterTitle: 'Выбор организаций',
      statusFilterTitle: 'Выбор статусов',
      organizationKindFilterTitle: 'Выбор типов организаций',
      unloadWithoutDocument: 'Выгружать организации без документов',
      unloadDefault: 'Выгружать значение по умолчанию при отсутствии значения в документе',
      applyNumberFormat: 'Применять числовой формат',
      sheets: {
        label: 'Выгружать листы',
        onlyHeads: 'Для головных учреждений',
        onlyChildren: 'Для филиалов',
        headsAndChildrens: 'Для головных учреждений и филиалов'
      },
      additionalColumns: {
        label: 'Дополнительные столбцы',
        curatorGroup: 'Кураторская группа',
        financingParagraph: 'Параграф финансирования'
      },
      emptyCell: 'Строка в пустой ячейке'
    }
  },
  documents: {
    name: 'Документы',
    version: 'Версия {version}',
    links: {
      sheets: 'Листы',
      attributes: 'Атрибуты',
      comments: 'Журнал'
    },
    tableHeaders: {
      version: 'Версия',
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
      status: '@:dcis.documents.addDocument.status'
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
    statusFilter: {
      title: 'Фильтр статусов',
      noFiltrationMessage: 'Все статусы',
      multipleMessage: '{name} и еще {restLength} статусов | {name} и еще {restLength} статус |' +
        ' {name} и еще {restLength} статуса'
    },
    unloadDocument: {
      name: 'Выгрузить документ',
      additional: 'Дополнительные колонки',
      rowAddDate: 'Дата добавления строки',
      rowUpdateDate: 'Дата последних изменений в строке',
      departmentName: 'Название департамента',
      departmentHead: 'Начальник департамента',
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
    },
    comments: {
      comment: 'Введите комментарий',
      send: '@:send'
    },
    attributes: {
      noAttributes: 'Нет атрибутов'
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
    sheetMenu: {
      editMenu: {
        buttonText: 'Правка',
        cut: 'Вырезать',
        cutShortcut: 'Ctrl+X',
        copy: 'Копировать',
        copyShortcut: 'Ctrl+C',
        paste: 'Вставить',
        pasteShortcut: 'Ctrl+V',
        shortcutDialog: {
          title: 'Копирование и вставка',
          message: 'Через меню "Правка" эта операция недоступна, однако можно использовать:',
          toCut: 'для вырезания',
          toCopy: 'для копирования',
          toPaste: 'для вставки'
        }
      },
      viewMenu: {
        buttonText: 'Вид',
        normalMode: 'Обычный режим',
        fullScreenMode: 'Полноэкранный режим'
      },
      documentUnloadMenu: {
        buttonText: 'Выгрузка',
        unload: '@:dcis.documents.unloadDocument.name'
      },
      recalculationMenu: {
        buttonText: 'Пересчет',
        recalculateAll: 'Пересчитать все'
      },
      tableSettings: {
        buttonText: '@:settings',
        showSettings: '@:dcis.sheets.settings.show'
      },
      reportUnloadMenu: {
        buttonText: '@:settings',
        documentFilter: '@:dcis.periods.report.documentsFilter.title',
        rowsFilter: '@:dcis.periods.report.rowsFilter.title'
      }
    },
    sheetToolbar: {
      formula: {
        tooltip: 'Формула',
        header: 'Изменение формулы',
        buttonText: '@:change',
        formula: 'Формула',
        recalculate: 'Пересчитать значения в документах'
      },
      aggregation: {
        tooltip: 'Агрегация ячеек',
        title: 'Настройки агрегации',
        choice: 'Метод агрегации',
        addCells: 'Добавить ячейки',
        defaultValue: 'Значение по умолчанию: {value}',
        kinds: {
          empty: 'Не задано',
          sum: 'Сумма',
          avg: 'Среднее арифметическое',
          max: 'Максимальное значение',
          min: 'Минимальное значение'
        }
      },
      readonly: 'Только для чтения',
      fix: 'Закрепление столбцов/строк',
      fontSize: 'Размер шрифта',
      kind: 'Тип',
      commaDecrease: 'Уменьшить разрядность',
      commaIncrease: 'Увеличить разрядность'
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
    columnLocalSettings: {
      header: 'Изменение локальных свойств',
      width: 'Ширина',
      reset: '@:reset',
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
    childRowSettings: {
      header: 'Изменение свойств',
      subheader: 'Дата изменения: {updatedAt}',
      height: 'Высота',
      buttonText: '@:save'
    },
    rowLocalSettings: {
      header: 'Изменение локальных свойств',
      height: 'Высота',
      reset: '@:reset',
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
    adds: 'Изменить атрибуты',
    add: 'Добавить атрибут',
    change: '@:change',
    delete: '@:delete',
    addMenu: {
      header: 'Добавление атрибута',
      buttonText: '@:add',
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
      buttonText: '@:change',
      name: 'Наименование',
      placeholder: 'Подсказка',
      key: 'Ключ',
      kind: 'Тип',
      default: 'Значение по умолчанию',
      mutable: 'Разрешить изменение'
    },
    AddAttributes: {
      buttonText: 'Добавить атрибут'
    },
    unloadAttributes: {
      buttonText: 'Выгрузить атрибуты'
    },
    uploadAttributes: {
      buttonText: 'Обновить атрибуты из файла',
      header: 'Обновление атрибутов из файла',
      attributesFile: 'Файл с новыми атрибутами',
      downloadTemplate: 'Скачать шаблон файла'
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
