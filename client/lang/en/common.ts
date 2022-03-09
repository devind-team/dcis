export default {
  dialogs: {
    chooseAvatarDialog: {
      chooseAvatar: 'Select avatar',
      avatar: 'Avatar',
      choose: 'Select avatar',
      delete: 'Delete avatar'
    },
    errorValidateDialog: {
      title: 'Validation errors',
      search: '@:search',
      rowNumber: 'Row #'
    },
    experimentalDialog: {
      title: 'In developing',
      subtitle: 'Message for user with devind_core.view_experimental permission',
      text: 'This functionality is under development.'
    }
  },
  menu: {
    confirmMenu: {
      yes: '@:yes',
      no: '@:no'
    },
    deleteMenu: {
      text: 'Are you sure you want to delete the {itemName}?',
      defaultItemName: 'record'
    }
  },
  filters: {
    baseDataFilter: {
      title: 'Filter',
      reset: '@:reset',
      apply: '@:apply'
    },
    itemsDataFilter: {
      search: '@:search',
      noFiltrationMessage: 'All records',
      multipleMessage: '{name} and {restLength} more records | {name} and {restLength} more record',
      selectAll: 'Select all'
    }
  },
  mutationResultAlert: {
    mutationBusinessLogicError: '@:mutationBusinessLogicError',
    mutationGraphQLError: '@:mutationGraphQLError',
    mutationNetworkError: '@:mutationNetworkError',
    tableMutationErrors: 'Errors occurred in validation',
    showDetails: 'Show details',
    mutationSuccess: '@:mutationSuccess'
  },
  fileField: {
    open: '@:open'
  },
  richTextEditor: {
    h1: 'Заголовок 1 уровня',
    h2: 'Заголовок 2 уровня',
    h3: 'Заголовок 3 уровня',
    preview: 'Предварительный просмотр',
    undo: 'Отменить',
    redo: 'Вернуть',
    bold: 'Жирный',
    italic: 'Курсив',
    strike: 'Зачеркнутый',
    bulletList: 'Список',
    orderedList: 'Нумерованный список',
    align: {
      left: 'Выровнять влево',
      right: 'Выровнять вправо',
      center: 'По центру',
      justify: 'По ширине'
    },
    removeLink: 'Удалить ссылку',
    image: 'Вставить изображение',
    imageField: 'Изображение',
    imageUpload: 'Загрузка изображения',
    file: 'Вставить файл',
    fileUpload: 'Загрузка файла',
    fileField: 'Файл',
    fileLabelField: 'Отображаемое название',
    highlight: 'Выделение текста',
    fontColor: 'Цвет шрифта',
    table: {
      insertTableHeader: 'Вставка таблицы',
      insertTable: 'Вставить таблицу',
      cols: 'Колонки',
      rows: 'Строки',
      firstRowIsHeader: 'Сделать первую строку заголовком',
      addColumnBefore: 'Вставить столбец до',
      addColumnAfter: 'Вставить столбец после',
      addRowBefore: 'Вставить строку до',
      addRowAfter: 'Вставить строку после',
      splitCell: 'Разделить ячейки',
      mergeCells: 'Слить ячейки',
      deleteRow: 'Удалить строку',
      deleteColumn: 'Удалить столбец',
      deleteTable: 'Удалить таблицу'
    },
    html: {
      insert: 'Вставить разметку'
    }
  }
}
