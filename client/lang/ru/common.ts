export default {
  dialogs: {
    chooseAvatarDialog: {
      chooseAvatar: 'Выбор аватара',
      avatar: 'Аватар',
      choose: 'Выбрать аватар',
      delete: 'Удалить аватар'
    },
    errorValidateDialog: {
      title: 'Ошибки валидации',
      search: '@:search',
      rowNumber: '№ строки'
    },
    experimentalDialog: {
      title: 'В разработке',
      subtitle: 'Сообщение для пользователя с разрешением devind_core.view_experimental',
      text: 'Данный функционал находится в разработке.'
    }
  },
  menu: {
    confirmMenu: {
      yes: '@:yes',
      no: '@:no'
    },
    deleteMenu: {
      text: 'Вы действительно хотите удалить {itemName}?',
      defaultItemName: 'запись'
    }
  },
  filters: {
    baseDataFilter: {
      title: 'Фильтр',
      reset: '@:reset',
      apply: '@:apply'
    },
    itemsDataFilter: {
      search: '@:search',
      noFiltrationMessage: 'Все записи',
      multipleMessage: '{name} и еще {restLength} записей | {name} и еще' +
        ' {restLength} запись | {name} и еще {restLength} записи',
      selectAll: 'Выбрать все'
    }
  },
  mutationResultAlert: {
    mutationBusinessLogicError: '@:mutationBusinessLogicError',
    mutationGraphQLError: '@:mutationGraphQLError',
    mutationNetworkError: '@:mutationNetworkError',
    tableMutationErrors: 'В валидации возникли ошибки',
    showDetails: 'Показать подробности',
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
    fullscreen: 'Полноэкранный режим',
    fullscreenExit: 'Выйти из полноэкранного режима',
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
    image: {
      image: 'Вставить изображение',
      px: 'В пикселях',
      pc: 'В процентах от размера родительского элемента',
      keepAspect: 'Сохранять пропорции',
      height: 'Высота',
      width: 'Ширина',
      changeImage: 'Изменить изображение'
    },
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
      insert: 'Редактировать разметку'
    },
    link: {
      insertLink: 'Вставить ссылку',
      label: 'Отображаемый текст',
      src: 'Адрес',
      openIn: 'Открыть ссылку в...',
      newWindow: 'Новом окне',
      currentWindow: 'Текущем окне'
    },
    lineHeight: {
      title: 'Межстрочный интервал',
      default: 'Стандартный'
    },
    underline: 'Подчеркнутый'
  },
  dropFileUpload: {
    dropOrClick: 'Перетащите файлы или нажмите на зону, чтобы загрузить'
  }
}
