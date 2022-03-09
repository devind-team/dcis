export default {
  eleden: '@:eleden.name',
  name: 'Справочники',
  search: '@:search',
  totalCount: '@:totalCount',
  shownOf: '@:shownOf',
  loadMore: '@:loadMore',
  yes: '@:yes',
  no: '@:no',
  fileKinds: {
    header: 'Типы файлов',
    tableHeaders: {
      id: '@:id',
      name: 'Тип файла',
      accept: 'Разрешенные файлы'
    }
  },
  directions: {
    header: 'Направления подготовки',
    tableHeaders: {
      id: '@:id',
      name: 'Направление подготовки',
      code: 'Код специальности',
      secret: 'Секретное направление',
      delete: 'Проводится обучение',
      eduServiceName: 'Услуга'
    }
  },
  eduServices: {
    header: 'Образовательные услуги',
    tableHeaders: {
      id: '@:id',
      name: '@:name'
    }
  },
  articleIndexes: {
    header: 'Индексирование статей',
    tableHeaders: {
      id: '@:id',
      name: '@:name',
      coefficient: 'Коэффициент учета'
    }
  },
  eduForms: {
    header: 'Формы обучения',
    tableHeaders: {
      id: '@:id',
      name: '@:name',
      shortName: 'Короткое название'
    }
  },
  disciplineViews: {
    header: 'Формы представления дисциплин',
    tableHeaders: {
      id: '@:id',
      name: '@:name'
    }
  },
  workKinds: {
    header: 'Виды работ',
    tableHeaders: {
      id: '@:id',
      name: '@:name',
      shortName: 'Короткое название',
      workFormName: 'Форма работы'
    }
  },
  workForms: {
    header: 'Формы работ',
    tableHeaders: {
      id: '@:id',
      name: '@:name'
    }
  },
  hoursKinds: {
    header: 'Типы часов',
    tableHeaders: {
      id: '@:id',
      name: '@:name'
    }
  },
  blockKinds: {
    header: 'Типы блоков образовательных программ',
    tableHeaders: {
      id: '@:id',
      name: '@:name'
    }
  },
  disciplineKinds: {
    header: 'Типы дисциплин',
    tableHeaders: {
      id: '@:id',
      name: '@:name'
    }
  },
  eduCycles: {
    header: 'Циклы образовательных программ',
    tableHeaders: {
      id: '@:id',
      name: '@:name',
      code: 'Код',
      blockKindName: 'Тип блока',
      disciplineKindName: 'Тип образовательной программы'
    }
  },
  periods: {
    header: 'Периоды',
    tableHeaders: {
      id: '@:id',
      name: '@:name',
      shortName: 'Короткое название'
    }
  },
  profiles: {
    header: '@:panel.dictionary.profile',
    tableHeaders: {
      id: '@:id',
      name: '@:name',
      code: 'Код',
      position: 'Порядок сортировки',
      kind: 'Тип'
    }
  }
}
