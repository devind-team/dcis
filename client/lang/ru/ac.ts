export default {
  eleden: '@:eleden.name',
  name: 'Группы и пользователи',
  teams: {
    name: 'Группы пользователей',
    index: 'Группа пользователей',
    buttons: {
      add: '@:add',
      upload: '@:upload'
    },
    search: '@:search',
    shownOf: '@:shownOf',
    tableHeaders: {
      name: '@:name',
      shortName: 'Краткое название',
      responsibleUsers: 'Ответственные',
      admission: 'Год набора/создания'
    },
    noSet: 'Не заданы',
    uploadTeams: {
      buttons: {
        uploadToExcel: 'Выгрузить в excel',
        uploadToCsv: 'Выгрузить в csv',
        uploadToJson: 'Выгрузить в json'
      }
    },
    menu: {
      users: '@:users',
      posts: 'Должности',
      portfolio: 'Портфолио',
      summaryReport: 'Ведомость с оценками',
      eduProgram: 'Образовательная программа',
      settings: '@:settings'
    },
    addMenu: {
      buttons: {
        add: '@:add',
        fillForm: '@:fillForm',
        fromFile: 'Добавить из файла (excel, json, csv)',
        helpInstruction: 'Инструкция по добавлению'
      },
      addForm: {
        header: 'Добавление группы',
        buttonText: '@:add'
      },
      fromFile: {
        header: 'Добавление групп пользователей',
        buttonText: '@:add'
      },
      helpDialog: {
        helpInstruction: '@:ac.teams.addMenu.buttons.helpInstruction'
      },
      form: {
        name: 'Название группы',
        shortName: 'Сокращенное название группы',
        admission: 'Год образования/набора',
        groupId: 'Назначать привилегии из группы',
        parentId: 'Родительская группа',
        file: 'Файл'
      }
    },
    jobKinds: {
      mj: 'Основное место работы',
      ip: 'Внутренний совместитель',
      ep: 'Внешний совместитель',
      cc: 'Договор гражданско правового характера'
    },
    users: {
      name: '@:ac.teams.menu.users',
      responsible: 'Ответственные:',
      noResponsible: 'не назначены',
      search: '@:search',
      shownOf: '@:shownOf',
      deleteItemName: 'пользователя',
      addMenu: {
        buttons: {
          add: '@:add',
          fromExisting: 'Выбрать из существующих',
          fromFileForExisting: 'Из файла для существующих',
          fromFileForNew: 'Из файла для новых',
          helpInstruction: 'Инструкция по добавлению'
        },
        fromExisting: {
          header: 'Добавление пользователя в группу',
          buttonText: '@:add'
        },
        fromFileForExisting: {
          header: 'Добавление существующих пользователей в группу',
          buttonText: '@:add'
        },
        fromFileForNew: {
          header: 'Добавление новых пользователей в группу',
          buttonText: '@:add'
        },
        helpDialog: {
          helpInstruction: '@:ac.teams.users.addMenu.buttons.helpInstruction'
        },
        form: {
          userId: 'Пользователь',
          rate: 'Занятость',
          postId: 'Должность',
          statusId: 'Статус',
          active: 'Активный',
          notActive: 'Неактивный',
          generateDocx: 'Создавать приказ в формате docx',
          generatePdf: 'Создавать приказ в формате pdf',
          statusCreatedAt: 'Дата присвоения статуса',
          file: 'Файл',
          kind: 'Тип работы',
          kindHint: 'Для студентов: Основное место работы'
        }
      },
      tableHeaders: {
        avatar: 'Аватар',
        name: 'ФИО',
        username: 'Логин',
        email: 'Email',
        actions: 'Действия'
      },
      tooltips: {
        delete: '@:delete'
      }
    },
    posts: {
      name: '@:ac.teams.menu.posts',
      search: '@:search',
      shownOf: '@:shownOf',
      deleteItemName: 'должность',
      addMenu: {
        buttons: {
          add: '@:add',
          fillForm: '@:fillForm'
        },
        addForm: {
          header: 'Добавление должностей',
          buttonText: '@:add'
        },
        form: {
          userId: 'Пользователь',
          rate: 'Занятость',
          postId: 'Должность',
          statusId: 'Статус',
          active: 'Активный',
          notActive: 'Неактивный',
          generateDocx: 'Создавать приказ в формате docx',
          generatePdf: 'Создавать приказ в формате pdf',
          statusCreatedAt: 'Дата присвоения статуса',
          kind: 'Тип работы',
          kindHint: 'Для студентов: Основное место работы'
        }
      },
      filters: {
        postFilter: {
          title: 'Фильтр должностей',
          noFiltrationMessage: 'Все должности'
        },
        jobKindFilter: {
          title: 'Фильтр типов работ',
          noFiltrationMessage: 'Все типы работ'
        }
      },
      tableHeaders: {
        avatar: 'Аватар',
        user: 'Пользователь',
        post: 'Должность',
        kind: 'Тип работы',
        rate: 'Занятость',
        actions: 'Действия'
      },
      tooltips: {
        change: '@:change',
        viewStatusHistory: 'Просмотреть историю статусов',
        addStatus: 'Добавить статус',
        delete: '@:delete'
      },
      statusHistory: {
        header: 'Статусы должности',
        tooltips: {
          downloadDocx: 'Скачать в формате docx',
          createDocx: 'Создать в формате docx',
          downloadPdf: 'Скачать в формате pdf',
          createPdf: 'Создать в формате pdf',
          delete: '@:delete'
        },
        tableHeaders: {
          status: 'Статус',
          active: 'Активен',
          createdAt: 'Дата получения',
          endAt: 'Дата потери',
          actions: 'Действия'
        }
      },
      statusHistoryAddForm: {
        header: 'Добавить статус',
        buttonText: '@:add',
        statusId: 'Статус',
        statusIdWarning: 'Такой незавершенный статус уже есть в истории',
        active: 'Активный',
        notActive: 'Неактивный',
        generateDocx: 'Создавать приказ в формате docx',
        generatePdf: 'Создавать приказ в формате pdf',
        statusCreatedAt: 'Дата присвоения статуса',
        completePrevious: 'Завершить предыдущие статусы'
      }
    },
    portfolio: {
      name: '@:ac.teams.menu.portfolio',
      search: '@:search',
      shownOf: '@:shownOf',
      addMenu: {
        buttons: {
          add: '@:add',
          fillForm: '@:fillForm',
          helpInstruction: 'Инструкция по добавлению'
        },
        addForm: {
          header: 'Добавление файлов в портфолио',
          buttonText: '@:add'
        },
        helpDialog: {
          helpInstruction: '@:ac.teams.portfolio.addMenu.buttons.helpInstruction'
        },
        form: {
          describe: 'Описание',
          disciplineId: 'Дисциплина',
          typeId: 'Тип файла',
          file: 'Архивный файл',
          confirm: 'Подтвердить файл'
        }
      },
      tableHeaders: {
        avatar: 'Аватар',
        user: 'Пользователь',
        discipline: '@:ac.teams.portfolio.addMenu.form.disciplineId',
        kind: 'Тип'
      }
    },
    eduProgram: {
      name: '@:ac.teams.menu.eduProgram',
      search: '@:search',
      shownOf: '@:shownOf',
      eduProgramNotSet: 'Образовательная программа не задана.',
      setEduProgram: 'Задать образовательную программу.'
    },
    summaryReport: {
      name: '@:ac.teams.menu.summaryReport',
      semester: 'Семестр №{number}',
      filters: {
        columnsFilter: {
          title: 'Фильтр столбцов',
          noFiltrationMessage: 'Все столбцы',
          noMarks: 'Нет оценок',
          anyMark: 'Хотя бы одна оценка',
          allMarks: 'Все оценки'
        },
        semestersFilter: {
          title: 'Фильтр семестров',
          noFiltrationMessage: 'Все семестры',
          multipleMessage: '{name} и еще {restLength} семестров | {name} и еще {restLength} семестр |' +
            ' {name} и еще {restLength} семестра'
        },
        workKindsFilter: {
          title: 'Фильтр видов аттестации',
          noFiltrationMessage: 'Все виды аттестации',
          multipleMessage: '{name} и еще {restLength} видов аттестации | {name} и еще {restLength} вид аттестации |' +
            ' {name} и еще {restLength} вида аттестации'
        },
        disciplinesFilter: {
          title: 'Фильтр дисциплин',
          noFiltrationMessage: 'Все дисциплины',
          multipleMessage: '{name} и еще {restLength} дисциплин | {name} и еще {restLength} дисциплина |' +
            ' {name} и еще {restLength} дисциплины'
        }
      },
      buttons: {
        upload: '@:upload'
      },
      dataTableHeaders: {
        user: 'Ф.И.О.'
      }
    },
    settings: {
      name: '@:ac.teams.menu.settings',
      updatedAt: '@:updatedAt',
      changeTeam: {
        form: {
          name: 'Название группы',
          shortName: 'Сокращенное название группы',
          admission: 'Год образования/набора',
          groupId: 'Назначать привилегии из группы',
          parentId: 'Родительская группа'
        },
        save: '@:save'
      },
      changeTeamResponsibleUsers: {
        name: 'Ответсвенные пользователи',
        mutationSuccess: 'Ответственные пользователи успешно заданы',
        save: '@:save'
      },
      changeTeamEduProgram: {
        name: '@:ac.teams.menu.eduProgram',
        setWarning: 'Внимание! Безопасно задать образовательную программу можно только один раз.',
        changeWarning: 'Внимание! Изменение образовательной программы может привести к несогласованности данных.',
        currentEduProgram: 'Текущая образовательная программа: ',
        set: '@:set',
        change: '@:change',
        form: {
          setHeader: 'Задание образовательной программы',
          changeHeader: 'Изменение образовательной программы',
          eduProgram: 'Образовательная программа',
          deleteCourses: 'Удалять курсы',
          transferCourses: 'Переносить курсы с удалением ненайденных',
          expedited: 'Ускоренная',
          search: '@:search',
          shownOf: '@:shownOf',
          tableHeaders: {
            code: 'Код',
            name: '@:name'
          },
          setButtonText: '@:set',
          changeButtonText: '@:change'
        }
      },
      changeTeamDelete: {
        name: 'Удаление',
        warning: 'Внимание! Удаление группы <b>нельзя</b> отменить.',
        delete: '@:delete',
        deleteItemName: 'группу',
        archived: 'Группа архивирована.',
        notArchived: 'Группа не архивирована.',
        archive: 'Архивировать',
        archiveConfirmText: 'Вы действительно хотите архивировать группу?',
        restore: 'Восстановить',
        restoreConfirmText: 'Вы действительно хотите восстановить группу?'
      }
    },
    teamActions: {
      sendNotification: 'Отправить уведомление',
      upload: '@:upload',
      unloadUsers: {
        header: 'Выгрузка пользователей',
        buttonText: 'Выгрузить',
        tableHeaders: {
          avatar: '@:ac.teams.portfolio.tableHeaders.avatar',
          username: 'Логин',
          lastName: 'Фамилия',
          firstName: 'Имя',
          sirName: 'Отчество'
        },
        html: 'Выгрузить в html',
        excel: 'Выгрузить в excel'
      },
      generateNewPasswords: {
        name: 'Сформировать новые пароли',
        search: '@:search',
        tableHeaders: {
          avatar: '@:ac.teams.portfolio.tableHeaders.avatar',
          username: 'Логин',
          lastName: 'Фамилия',
          firstName: 'Имя',
          sirName: 'Отчество'
        },
        generatingNewPasswords: 'Генерация новых паролей для группы ',
        generatePasswords: 'Сгенерировать',
        generationDate: 'Дата генерации'
      }
    }
  },
  users: {
    name: '@:users',
    buttons: {
      add: '@:add',
      upload: '@:upload'
    },
    search: '@:search',
    shownOf: '@:shownOf',
    userAvatar: 'Аватар пользователя',
    tableHeaders: {
      avatar: '@:ac.teams.portfolio.tableHeaders.avatar',
      name: 'ФИО',
      username: 'Логин',
      email: 'Email',
      groups: 'Группы',
      createdAt: 'Регистрация'
    },
    menu: {
      personalities: 'Персоналии',
      profile: 'Профиль',
      portfolio: '@:ac.teams.menu.portfolio',
      articles: '@:articles.name'
    },
    addMenu: {
      buttons: {
        fromFile: 'Добавить из файла (excel, csv, json)',
        helpInstruction: 'Инструкция по добавлению'
      },
      addForm: {
        header: 'Добавление пользователей из файла',
        buttonText: '@:add'
      },
      helpDialog: {
        helpInstruction: '@:ac.users.addMenu.buttons.helpInstruction'
      },
      form: {
        file: 'Файл с пользователями',
        groups: 'Группы'
      }
    },
    portfolio: {
      name: '@:ac.users.menu.portfolio',
      search: '@:search',
      shownOf: '@:shownOf',
      addMenu: {
        buttons: {
          add: '@:add',
          fillForm: '@:fillForm'
        },
        addForm: {
          header: 'Добавление файла в портфолио',
          buttonText: '@:add'
        },
        form: {
          describe: '@:ac.teams.portfolio.addMenu.form.describe',
          disciplineId: '@:ac.teams.portfolio.addMenu.form.disciplineId',
          typeId: '@:ac.teams.portfolio.addMenu.form.typeId',
          file: '@:ac.teams.addMenu.form.file',
          confirm: '@:ac.teams.portfolio.addMenu.form.confirm'
        }
      },
      tableHeaders: {
        describe: '@:ac.teams.portfolio.addMenu.form.describe',
        discipline: '@:ac.teams.portfolio.addMenu.form.disciplineId',
        kind: '@:ac.teams.portfolio.tableHeaders.kind'
      },
      tableSubheaders: {
        key: 'Ключ',
        value: 'Значение'
      },
      buttons: {
        delete: '@:delete',
        open: '@:open'
      },
      subTableKeys: {
        createdAt: 'Дата создания',
        updatedAt: 'Дата обновления',
        describe: '@:ac.teams.portfolio.addMenu.form.describe',
        user: 'Подтверждение',
        file: '@:ac.teams.addMenu.form.file',
        delete: 'Удаление'
      },
      confirmation: {
        confirm: 'Подтвердить',
        confirmQuestion: 'Вы уверены, что хотите подтвердить файл?',
        notConfirmed: 'Не подтвержден',
        yes: '@:yes',
        no: '@:no'
      }
    },
    articles: {
      name: 'Публикации'
    },
    profile: {
      name: '@:ac.users.menu.profile',
      tableHeaders: {
        name: 'Наименование',
        value: 'Значение'
      }
    },
    personalities: {
      name: '@:ac.users.menu.personalities',
      createdAt: 'Дата регистрации: ',
      buttons: {
        blockUser: 'Заблокировать пользователя',
        unblockUser: 'Разблокировать пользователя'
      },
      tableHeaders: {
        avatar: '@:ac.teams.portfolio.tableHeaders.avatar',
        personalities: 'Персональные данные',
        responsible: 'Ответственный за группы',
        jobs: '@:ac.users.tableHeaders.groups',
        blocking: 'Блокировка'
      },
      helpText: 'Заблокированный пользователь выбрасывается из сети и не имеет возможности авторизоваться.',
      changeAvatar: {
        avatar: '@:ac.teams.portfolio.tableHeaders.avatar',
        chooseAvatar: 'Выбрать аватар',
        buttons: {
          changeAvatar: 'Изменить аватар',
          load: '@:load'
        }
      },
      responsible: {
        admission: 'Год набора/образования: '
      },
      personalities: {
        tableHeaders: {
          text: 'Поле',
          value: 'Значение'
        }
      },
      jobs: {
        tableHeaders: {
          team: 'Группа',
          post: 'Должность'
        }
      }
    },
    components: {
      addUsersMenu: {
        fromFile: 'Из файла (excel, csv, json)',
        loadUsers: 'Загрузка пользователей из файла',
        error: 'Во валидации возникли ошибки. Показать подробности.',
        load: '@:load'
      },
      avatarDialog: {
        UserAvatar: 'Аватар пользователя:'
      },
      avatarView: {
        changeAvatar: 'Изменить аватар'
      },
      changeUsers: {
        users: 'Пользователи'
      },
      resetPasswords: {
        resetPassword: 'Сбросить пароль'
      },
      sendNotification: {
        sendNotification: 'Отправить уведомление'
      },
      unloadUsersMenu: {
        uploadToExcel: 'Выгрузить в xlsx файл',
        uploadToCsv: 'Выгрузить в csv файл'
      }
    }
  },
  filters: {
    disciplineFilter: {
      title: 'Фильтр дисциплин',
      noFiltrationMessage: 'Все дисциплины',
      multipleMessage: '{name} и еще {restLength} дисциплин | {name} и еще {restLength} дисциплина |' +
        ' {name} и еще {restLength} дисциплины'
    },
    fileKindFilter: {
      title: 'Фильтр типов',
      noFiltrationMessage: 'Все типы',
      multipleMessage: '{name} и еще {restLength} типов | {name} и еще {restLength} тип |' +
        ' {name} и еще {restLength} типа'
    }
  }
}
