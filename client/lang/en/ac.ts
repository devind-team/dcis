export default {
  eleden: '@:eleden.name',
  name: 'Groups and users',
  teams: {
    name: 'Users groups',
    index: 'Users group',
    buttons: {
      add: '@:add',
      upload: '@:upload'
    },
    search: '@:search',
    shownOf: '@:shownOf',
    tableHeaders: {
      name: '@:name',
      shortName: 'Short name',
      responsibleUsers: 'Responsible users',
      admission: 'Recruitment/creation year'
    },
    noSet: 'Not set',
    uploadTeams: {
      buttons: {
        uploadToExcel: 'Upload to excel',
        uploadToCsv: 'Upload to csv',
        uploadToJson: 'Upload to json'
      }
    },
    menu: {
      users: '@:users',
      posts: 'Posts',
      portfolio: 'Portfolio',
      summaryReport: 'Statement with marks',
      eduProgram: 'Educational program',
      settings: '@:settings'
    },
    addMenu: {
      buttons: {
        add: '@:add',
        fillForm: '@:fillForm',
        fromFile: 'Add from file (excel, json, csv)',
        helpInstruction: 'Instruction to add'
      },
      addForm: {
        header: 'Add group',
        buttonText: '@:add'
      },
      fromFile: {
        header: 'Add users groups',
        buttonText: '@:add'
      },
      helpDialog: {
        helpInstruction: '@:ac.teams.addMenu.buttons.helpInstruction'
      },
      form: {
        name: 'Group name',
        shortName: 'Short group name',
        admission: 'Creation/Recruitment year',
        groupId: 'Set permissions from group',
        parentId: 'Parent group',
        file: 'File'
      }
    },
    jobKinds: {
      mj: 'Main job',
      ip: 'Internal part-time',
      ep: 'External part-time',
      cc: 'Civil contract'
    },
    users: {
      name: '@:ac.teams.menu.users',
      responsible: 'Responsible users:',
      noResponsible: 'not set',
      search: '@:search',
      shownOf: '@:shownOf',
      deleteItemName: 'user',
      addMenu: {
        buttons: {
          add: '@:add',
          fromExisting: 'Select from existing',
          fromFileForExisting: 'From file for existing',
          fromFileForNew: 'From file for new',
          helpInstruction: 'Instruction to add'
        },
        fromExisting: {
          header: 'Add user to the group',
          buttonText: '@:add'
        },
        fromFileForExisting: {
          header: 'Add existing users to the group',
          buttonText: '@:add'
        },
        fromFileForNew: {
          header: 'Add new users to the group',
          buttonText: '@:add'
        },
        helpDialog: {
          helpInstruction: '@:ac.teams.users.addMenu.buttons.helpInstruction'
        },
        form: {
          userId: 'User',
          rate: 'Employment rate',
          postId: 'Position',
          statusId: 'Status',
          active: 'Active',
          notActive: 'Not active',
          generateDocx: 'Create decree in docx format',
          generatePdf: 'Create decree in pdf format',
          statusCreatedAt: 'Status assignment date',
          file: 'File',
          kind: 'Job kind',
          kindHint: 'For students: Main job'
        }
      },
      tableHeaders: {
        avatar: 'Avatar',
        name: 'Full name',
        username: 'Login',
        email: 'Email',
        actions: 'Actions'
      },
      tooltips: {
        delete: '@:delete'
      }
    },
    posts: {
      name: '@:ac.teams.menu.posts',
      search: '@:search',
      shownOf: '@:shownOf',
      deleteItemName: 'post',
      addMenu: {
        buttons: {
          add: '@:add',
          fillForm: '@:fillForm'
        },
        addForm: {
          header: 'Add posts',
          buttonText: '@:add'
        },
        form: {
          userId: 'User',
          rate: 'Employment rate',
          postId: 'Position',
          statusId: 'Status',
          active: 'Active',
          notActive: 'Not active',
          generateDocx: 'Create decree in docx format',
          generatePdf: 'Create decree in pdf format',
          statusCreatedAt: 'Status assignment date',
          kind: 'Job kind',
          kindHint: 'For students: Main job'
        }
      },
      filters: {
        postFilter: {
          title: 'Post filter',
          noFiltrationMessage: 'All posts'
        },
        jobKindFilter: {
          title: 'Work kind filter',
          noFiltrationMessage: 'All work kinds'
        }
      },
      tableHeaders: {
        avatar: 'Avatar',
        user: 'User',
        post: 'Position',
        kind: 'Job kind',
        rate: 'Rate',
        actions: 'Actions'
      },
      tooltips: {
        change: '@:change',
        viewStatusHistory: 'View status history',
        addStatus: 'Add status',
        delete: '@:delete'
      },
      statusHistory: {
        header: 'Статусы должности',
        tooltips: {
          downloadDocx: 'Download in docx format',
          createDocx: 'Create in docx format',
          downloadPdf: 'Download in pdf format',
          createPdf: 'Create in pdf format',
          delete: '@:delete'
        },
        tableHeaders: {
          status: 'Status',
          active: 'Active',
          createdAt: 'Created at',
          endAt: 'End at',
          actions: 'Actions'
        }
      },
      statusHistoryAddForm: {
        header: 'Add status',
        buttonText: '@:add',
        statusId: 'Status',
        statusIdWarning: 'This incomplete status already exists in history',
        active: 'Active',
        notActive: 'Not active',
        generateDocx: 'Create decree in docx format',
        generatePdf: 'Create decree in pdf format',
        statusCreatedAt: 'Status assignment date',
        completePrevious: 'Complete previous statuses'
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
          helpInstruction: 'Instruction to add'
        },
        addForm: {
          header: 'Add files to portfolio',
          buttonText: '@:add'
        },
        helpDialog: {
          helpInstruction: '@:ac.teams.portfolio.addMenu.buttons.helpInstruction'
        },
        form: {
          describe: 'Description',
          disciplineId: 'Discipline',
          typeId: 'File type',
          file: 'Archive file',
          confirm: 'Confirm file'
        }
      },
      tableHeaders: {
        avatar: 'Avatar',
        user: 'User',
        discipline: '@:ac.teams.portfolio.addMenu.form.disciplineId',
        kind: 'Type'
      }
    },
    eduProgram: {
      name: '@:ac.teams.menu.eduProgram',
      search: '@:search',
      shownOf: '@:shownOf',
      eduProgramNotSet: 'Educational program not set.',
      setEduProgram: 'Set educational program.'
    },
    summaryReport: {
      name: '@:ac.teams.menu.summaryReport',
      semester: 'Semester №{number}',
      filters: {
        columnsFilter: {
          title: 'Columns filter',
          noFiltrationMessage: 'All columns',
          noMarks: 'No marks',
          anyMark: 'At least one mark',
          allMarks: 'All marks'
        },
        semestersFilter: {
          title: 'Semester filter',
          noFiltrationMessage: 'All semesters',
          multipleMessage: '{name} and {restLength} more semesters | {name} and {restLength} more semesters |' +
            ' {name} and {restLength} more semesters'
        },
        workKindsFilter: {
          title: 'Attestation types filter',
          noFiltrationMessage: 'All attestation types',
          multipleMessage: '{name} and {restLength} more attestation types |' +
            ' {name} and {restLength} more attestation types |' +
            ' {name} and {restLength} more attestation types'
        },
        disciplinesFilter: {
          title: 'Discipline filter',
          noFiltrationMessage: 'All disciplines',
          multipleMessage: '{name} and {restLength} more disciplines | {name} and {restLength} more disciplines |' +
            ' {name} and {restLength} more disciplines'
        }
      },
      buttons: {
        upload: '@:upload'
      },
      dataTableHeaders: {
        user: 'Full name'
      }
    },
    settings: {
      name: '@:ac.teams.menu.settings',
      updatedAt: '@:updatedAt',
      changeTeam: {
        form: {
          name: 'Group name',
          shortName: 'Short group name',
          admission: 'Creation/Recruitment year',
          groupId: 'Set permissions from group',
          parentId: 'Parent group'
        },
        save: '@:save'
      },
      changeTeamResponsibleUsers: {
        name: 'Responsible users',
        mutationSuccess: 'Responsible users was set successfully',
        save: '@:save'
      },
      eduProgram: {
        name: '@:ac.teams.menu.eduProgram',
        setWarning: 'Attention! You can safely set the educational program only once.',
        changeWarning: 'Attention! Changes to the educational program may lead to data inconsistencies.',
        currentEduProgram: 'Current educational program: ',
        set: '@:set',
        change: '@:change',
        form: {
          setHeader: 'Set educational program',
          changeHeader: 'Change educational program',
          deleteCourses: 'Delete courses',
          transferCourses: 'Transfer courses with deletion of not found ones',
          expedited: 'Expedited',
          eduProgram: 'Educational program',
          search: '@:search',
          shownOf: '@:shownOf',
          tableHeaders: {
            code: 'Code',
            name: '@:name'
          },
          setButtonText: '@:set',
          changeButtonText: '@:change'
        }
      },
      changeTeamDelete: {
        name: 'Delete',
        warning: 'Attention! Deleting the group <b>cannot</b> be undone.',
        delete: '@:delete',
        deleteItemName: 'group',
        archived: 'The group is archived.',
        notArchived: 'The group is not archived.',
        archive: 'Archive',
        archiveConfirmText: 'Are you sure you want to archive the group?',
        restore: 'Restore',
        restoreConfirmText: 'Are you sure you want to restore the group?'
      }
    },
    teamActions: {
      sendNotification: 'Send notification',
      upload: '@:upload',
      generateNewPasswords: {
        name: 'Generate new passwords',
        search: '@:search',
        tableHeaders: {
          avatar: '@:ac.teams.portfolio.tableHeaders.avatar',
          username: 'Login',
          lastName: 'Last name',
          firstName: 'First name',
          sirName: 'Middle name'
        },
        generatingNewPasswords: 'Generate new passwords for group',
        generatePasswords: 'Generate',
        generationDate: 'Generation date'
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
    userAvatar: 'User avatar',
    tableHeaders: {
      avatar: '@:ac.teams.portfolio.tableHeaders.avatar',
      name: 'Full name',
      username: 'Login',
      email: 'Email',
      groups: 'Groups',
      createdAt: 'Registration'
    },
    menu: {
      personalities: 'Personalities',
      profile: 'Profile',
      portfolio: '@:ac.teams.menu.portfolio',
      articles: '@:articles.name'
    },
    addMenu: {
      buttons: {
        fromFile: 'Add from file (excel, json, csv)',
        helpInstruction: 'Instruction to add'
      },
      addForm: {
        header: 'Add users from file',
        buttonText: '@:add'
      },
      helpDialog: {
        helpInstruction: '@:ac.users.addMenu.buttons.helpInstruction'
      },
      form: {
        file: 'File with users',
        groups: 'Groups'
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
          header: 'Add file to portfolio',
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
        key: 'Key',
        value: 'Value'
      },
      buttons: {
        delete: '@:delete',
        open: '@:open'
      },
      subTableKeys: {
        createdAt: 'Creation date',
        updatedAt: 'Updating date',
        describe: '@:ac.teams.portfolio.addMenu.form.describe',
        user: 'Confirm',
        file: '@:ac.teams.addMenu.form.file',
        delete: 'Delete'
      },
      confirmation: {
        confirm: 'Confirm',
        confirmQuestion: 'Are you sure, you want to confirm the file?',
        notConfirmed: 'Not confirmed',
        yes: '@:yes',
        no: '@:no'
      }
    },
    articles: {
      name: 'Articles'
    },
    profile: {
      name: '@:ac.users.menu.profile',
      tableHeaders: {
        name: '@:name',
        value: 'Value'
      }
    },
    personalities: {
      name: '@:ac.users.menu.personalities',
      createdAt: 'Registration date: ',
      buttons: {
        blockUser: 'Block user',
        unblockUser: 'Unblock user'
      },
      tableHeaders: {
        avatar: '@:ac.teams.portfolio.tableHeaders.avatar',
        personalities: 'Personal data',
        responsible: 'Responsible for groups',
        jobs: '@:ac.users.tableHeaders.groups',
        blocking: 'Block'
      },
      helpText: 'Blocked user is removed from the network and cannot be authorized.',
      changeAvatar: {
        avatar: '@:ac.teams.portfolio.tableHeaders.avatar',
        chooseAvatar: 'Select avatar',
        buttons: {
          changeAvatar: 'Edit avatar',
          load: '@:load'
        }
      },
      responsible: {
        admission: 'Recruitment/creation year: '
      },
      personalities: {
        tableHeaders: {
          text: 'Field',
          value: 'Value'
        }
      },
      jobs: {
        tableHeaders: {
          team: 'Group',
          post: 'Position'
        }
      }
    },
    components: {
      addUsersMenu: {
        fromFile: 'From file (excel, csv, json)',
        loadUsers: 'Upload users from file',
        error: 'User validation failed. Show details.',
        load: '@:load'
      },
      avatarDialog: {
        UserAvatar: 'User avatar:'
      },
      avatarView: {
        changeAvatar: 'Edit avatar'
      },
      changeUsers: {
        users: 'Users'
      },
      resetPasswords: {
        resetPassword: 'Reset password'
      },
      sendNotification: {
        sendNotification: 'Send notification'
      },
      unloadUsersMenu: {
        uploadToExcel: 'Upload to excel',
        uploadToCsv: 'Upload to csv'
      }
    }
  },
  filters: {
    disciplineFilter: {
      title: 'Discipline filter',
      noFiltrationMessage: 'All disciplines',
      multipleMessage: '{name} and {restLength} more disciplines | {name} and {restLength} more disciplines |' +
        ' {name} and {restLength} more disciplines'
    },
    fileKindFilter: {
      title: 'Type filter',
      noFiltrationMessage: 'All types',
      multipleMessage: '{name} and {restLength} more types | {name} and {restLength} more types |' +
        ' {name} and {restLength} more types'
    }
  }
}
