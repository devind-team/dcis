export default {
  name: 'Ход образовательного процесса',
  teams: {
    name: 'Группы пользователей c курсами',
    buttons: {
      add: '@:add'
    },
    addMenu: {
      buttons: {
        fillForm: '@:fillForm',
        addFromFile: 'Добавить из файла (excel, json, csv)',
        helpInstruction: 'Инструкция по добавлению'
      },
      addForm: {
        header: 'Добавление курсов',
        buttonText: '@:add'
      },
      helpDialog: {
        helpInstruction: '@:process.teams.addMenu.buttons.helpInstruction'
      }
    },
    search: '@:search',
    shownOf: '@:shownOf',
    tableHeaders: {
      name: 'Название',
      shortName: 'Краткое название',
      responsibleUsers: 'Ответственные',
      admission: 'Год набора/создания',
      actions: 'Действия'
    },
    tableItem: {
      noSet: 'Не заданы',
      actions: {
        change: '@:change',
        delete: '@:delete'
      },
      goToUser: 'Перейти к пользователю',
      deleteItemName: 'все курсы группы'
    },
    courseForm: {
      team: 'Группа',
      noEduProgram: 'У группы отсутствует образовательная программа',
      courseNumber: 'Номер курса',
      semesterNumber: 'Номер семестра',
      discipline: 'Дисциплина',
      noDisciplines: 'Дисциплины, которым можно добавить курсы, отсутствуют',
      baseTableHeaders: {
        workKind: 'Вид работы',
        teachers: 'Преподаватели'
      },
      tableErrors: {
        validationError: 'Необходимо правильно заполнить курсы',
        atLeastOneCourseError: 'Необходимо выбрать как минимум один курс'
      },
      tableTooltips: {
        pickAllPeriods: 'Выбрать все периоды',
        pickRowPeriods: 'Выбрать периоды строки'
      },
      tableItem: {
        hours: '{count} часов | {count} час | {count} часа',
        teachers: '@:process.courseForm.baseTableHeaders.teachers',
        statuses: {
          exclude: 'Курс не будет добавлен',
          add: 'Курс будет добавлен',
          noTeachers: 'Требуется выбрать хотя бы одного преподавателя',
          noPeriods: 'Требуется отметить хотя бы один период'
        }
      }
    },
    changeForm: {
      header: 'Изменение курсов',
      buttonText: '@:change'
    }
  },
  team: {
    name: 'Курсы',
    process: '@:process.name',
    filters: {
      semesterFilter: {
        title: 'Фильтр семестров',
        semester: 'Семестр №{number}',
        noFiltrationMessage: 'Все семестры'
      },
      disciplinesFilter: {
        title: 'Фильтр дисциплин',
        noFiltrationMessage: 'Все дисциплины',
        multipleMessage: '{name} и еще {restLength} дисциплин | {name} и еще {restLength} дисциплина |' +
          ' {name} и еще {restLength} дисциплины'
      },
      workKindsFilter: {
        title: 'Фильтр типов работ',
        noFiltrationMessage: 'Все типы работ',
        multipleMessage: '{name} и еще {restLength} типов работы | {name} и еще {restLength} тип работы |' +
          ' {name} и еще {restLength} типа работы'
      },
      teachersFilter: {
        title: 'Фильтр преподавателей',
        noFiltrationMessage: 'Все преподаватели',
        multipleMessage: '{name} и еще {restLength} преподавателей | {name} и еще {restLength} преподаватель |' +
          ' {name} и еще {restLength} преподавателя'
      }
    },
    search: '@:search',
    shownOf: '@:shownOf',
    tableHeaders: {
      semester: 'Семестр',
      name: 'Название',
      teachers: 'Преподаватели',
      actions: 'Действия'
    },
    tableItem: {
      noSet: 'Не заданы',
      goToUser: 'Перейти к пользователю',
      actions: {
        change: '@:change',
        delete: '@:delete'
      },
      deleteItemName: 'курс'
    }
  },
  course: {
    name: '{name} ({count} часов) | {name} ({count} час) | {name} ({count} часа)',
    process: '@:process.name',
    chat: {
      name: 'Чат',
      messagePlaceholder: 'Напишите сообщение...'
    },
    handout: {
      name: 'Методические рекомендации',
      search: '@:search',
      shownOf: '@:shownOf',
      deleteItemName: 'раздаточный материал',
      tableHeaders: {
        description: 'Описание',
        user: 'Пользователь',
        file: 'Файл',
        course: 'Курс',
        period: 'Период обучения',
        actions: 'Действия',
        createdAt: 'Дата создания'
      },
      filters: {
        periodFilter: {
          noFiltrationMessage: 'Все периоды',
          title: 'Фильтр периодов',
          multipleMessage: '{name} и еще {restLength} периодов | {name} и еще {restLength} период |' +
            ' {name} и еще {restLength} период'
        }
      },
      buttons: {
        add: '@:add',
        fillForm: 'Заполнить форму'
      },
      tooltips: {
        delete: '@:delete'
      },
      addForm: {
        description: 'Описание',
        file: 'Файл',
        period: 'Период обучения',
        course: 'Курс',
        buttonText: '@:add',
        header: 'Добавление методических рекомендаций'
      }
    },
    register: {
      name: 'Журнал',
      responsibleUsers: 'Ответственные',
      teachers: 'Преподаватели',
      baseTableHeaders: {
        students: 'Ф.И.О.'
      },
      handout: '@:process.course.handout.name',
      changeAttestations: {
        mutationBusinessLogicError: '@:mutationBusinessLogicError',
        mutationSuccess: '@:mutationSuccess',
        deleteSuccess: '@:deleteSuccess',
        changeAttendance: {
          setBy: 'Выставил',
          confirmedBy: 'Подтвердил',
          attendanceNotSet: 'Отсутствие на занятии не задано',
          attendance: 'Отсутствие на занятии',
          confirm: 'Подтвердить',
          change: '@:change',
          cancel: '@:cancel',
          delete: '@:delete',
          save: '@:save'
        },
        changeMark: {
          setBy: 'Выставил',
          markNotSet: 'Оценка не выставлена',
          mark: 'Оценка',
          description: 'Комментарий',
          change: '@:change',
          cancel: '@:cancel',
          delete: '@:delete',
          save: '@:save'
        },
        changeAttachments: {
          attachments: 'Прикрепленные файлы',
          zeroAttachments: 'Прикрепленные файлы отсутствуют',
          newPortfolioFiles: 'Новые файлы из портфолио',
          confirmed: 'подтвержден',
          notConfirmed: 'не подтвержден',
          newFiles: 'Новые файлы',
          describe: 'Описание',
          fileKind: 'Тип файлов',
          confirm: 'Подтвердить',
          open: '@:open',
          change: '@:change',
          cancel: '@:cancel',
          save: '@:save'
        }
      },
      changeHandouts: {
        title: '@:process.course.handout.name',
        mutationBusinessLogicError: '@:mutationBusinessLogicError',
        mutationSuccess: '@:mutationSuccess',
        zeroHandouts: 'Методические рекомендации отсутствуют',
        newFile: 'Новый файл',
        description: 'Описание',
        open: '@:open',
        change: '@:change',
        cancel: '@:cancel',
        save: '@:save'
      }
    },
    webinars: {
      name: 'Вебинары'
    }
  }
}
