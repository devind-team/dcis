export default {
  name: 'Educational process',
  teams: {
    name: 'User groups with course',
    buttons: {
      add: '@:add'
    },
    addMenu: {
      buttons: {
        fillForm: '@:fillForm',
        addFromFile: 'Add from file (excel, json, csv)',
        helpInstruction: 'Instruction to add'
      },
      addForm: {
        header: 'Add courses',
        buttonText: '@:add'
      },
      helpDialog: {
        helpInstruction: '@:process.teams.addMenu.buttons.helpInstruction'
      }
    },
    search: '@:search',
    shownOf: '@:shownOf',
    tableHeaders: {
      name: '@:name',
      shortName: 'Short name',
      responsibleUsers: 'Responsible users',
      admission: 'Recruitment/creation year',
      actions: 'Actions'
    },
    tableItem: {
      noSet: 'Not set',
      actions: {
        change: '@:change',
        delete: '@:delete'
      },
      goToUser: 'Go to user',
      deleteItemName: 'all courses group'
    },
    courseForm: {
      team: 'Group',
      noEduProgram: 'Group has no educational program',
      courseNumber: 'Course number',
      semesterNumber: 'Semester number',
      discipline: 'Discipline',
      noDisciplines: 'There are no disciplines which can be added to courses',
      baseTableHeaders: {
        workKind: 'Type of work',
        teachers: 'Lecturers'
      },
      tableErrors: {
        validationError: 'All courses must be filled correctly',
        atLeastOneCourseError: 'You must select at least one course'
      },
      tableTooltips: {
        pickAllPeriods: 'Pick all periods',
        pickRowPeriods: 'Pick row periods'
      },
      tableItem: {
        hours: '{count} hours | {count} hour | {count} hours',
        teachers: '@:process.courseForm.baseTableHeaders.teachers',
        statuses: {
          exclude: 'Course will not be added',
          add: 'Course will be added',
          noTeachers: 'You must select at least one teacher',
          noPeriods: 'It is required to mark at least one period'
        }
      }
    },
    changeForm: {
      header: 'Edit courses',
      buttonText: '@:change'
    }
  },
  team: {
    name: 'Courses',
    process: '@:process.name',
    filters: {
      semesterFilter: {
        title: 'Semesters filter',
        semester: 'Semester №{number}',
        noFiltrationMessage: 'All semesters'
      },
      disciplinesFilter: {
        title: 'Disciplines filter',
        noFiltrationMessage: 'All disciplines',
        multipleMessage: '{name} and {restLength} more disciplines | {name} and {restLength} more discipline |' +
          ' {name} and {restLength} more disciplines'
      },
      workKindsFilter: {
        title: 'Types of work filter',
        noFiltrationMessage: 'All types of work',
        multipleMessage: '{name} and {restLength} more types of work | {name} and {restLength} more type of work |' +
          ' {name} and {restLength} more types of work'
      },
      teachersFilter: {
        title: 'Lecturers filter',
        noFiltrationMessage: 'All lecturers',
        multipleMessage: '{name} and {restLength} more lecturers | {name} and {restLength} more lecturer |' +
          ' {name} and {restLength} more lecturers'
      }
    },
    search: '@:search',
    shownOf: '@:shownOf',
    tableHeaders: {
      semester: 'Semester',
      name: '@:name',
      teachers: 'Lecturers',
      actions: 'Actions'
    },
    tableItem: {
      goToUser: 'Go to user',
      actions: {
        change: '@:change',
        delete: '@:delete'
      },
      deleteItemName: 'course'
    }
  },
  course: {
    name: '{name} ({count} hours) | {name} ({count} hour) | {name} ({count} hour)',
    process: '@:process.name',
    chat: {
      name: 'Member.vue',
      messagePlaceholder: 'Type message...'
    },
    handout: {
      name: 'Handouts',
      search: '@:search',
      shownOf: '@:shownOf',
      deleteItemName: 'handout',
      tableHeaders: {
        description: 'Description',
        user: 'User',
        file: 'File',
        course: 'Course',
        period: 'Period of study',
        actions: 'Actions',
        createdAt: 'Creation date'
      },
      filters: {
        periodFilter: {
          noFiltrationMessage: 'All periods',
          title: 'Periods filter',
          multipleMessage: '{name} and {restLength} more periods | {name} and {restLength} more period |' +
            ' {name} and {restLength} more periods'
        }
      },
      buttons: {
        add: '@:add',
        fillForm: '@:fillForm'
      },
      tooltips: {
        delete: '@:delete'
      },
      addForm: {
        description: 'Description',
        file: 'File',
        period: 'Period of study',
        course: 'Course',
        buttonText: '@:add',
        header: 'Add handouts'
      }
    },
    register: {
      name: 'Register',
      responsibleUsers: 'Responsible users',
      teachers: 'Lecturers',
      baseTableHeaders: {
        students: 'Full name'
      },
      handout: '@:process.course.handout.name',
      changeAttestations: {
        mutationBusinessLogicError: '@:mutationBusinessLogicError',
        mutationSuccess: '@:mutationSuccess',
        deleteSuccess: '@:deleteSuccess',
        changeAttendance: {
          setBy: 'Set by',
          confirmedBy: 'Confirmed',
          attendanceNotSet: 'Attended',
          attendance: 'Not attended',
          confirm: 'Confirm',
          change: '@:change',
          cancel: '@:cancel',
          delete: '@:delete',
          save: '@:save'
        },
        changeMark: {
          setBy: 'Graded',
          markNotSet: 'Mark is not graded',
          mark: 'Mark',
          description: 'Comment',
          change: '@:change',
          cancel: '@:cancel',
          delete: '@:delete',
          save: '@:save'
        },
        changeAttachments: {
          attachments: 'Attached files',
          zeroAttachments: 'No attached files',
          newPortfolioFiles: 'New portfolio files',
          confirmed: 'confirmed',
          notConfirmed: 'not confirmed',
          newFiles: 'New files',
          describe: 'Description',
          fileKind: 'Files type',
          confirm: 'Confirm',
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
        zeroHandouts: 'No handouts',
        newFile: 'New file',
        description: 'Description',
        open: '@:open',
        change: '@:change',
        cancel: '@:cancel',
        save: '@:save'
      }
    },
    webinars: {
      name: 'Webinars'
    }
  }
}
