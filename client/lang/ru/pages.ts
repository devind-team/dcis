export default {
  index: 'Странички',
  categories: 'Категории',
  category: {
    addCardHeader: 'Добавить категорию',
    addDialog: {
      header: 'Добавление категории',
      parentCategory: 'Родительская категория',
      avatar: 'Аватар',
      text: 'Название категории',
      add: 'Добавить'
    },
    position: 'Порядок сортировки',
    parentId: 'Родительская категория',
    noCategories: 'Категорий еще нет.'
  },
  page: {
    addCardHeader: 'Добавить страницу',
    add: {
      header: 'Добавление страницы',
      category: 'Категория',
      avatar: 'Аватар',
      title: 'Заголовок',
      signature: 'Подпись страницы',
      kind: 'Тип',
      parallax: 'Параллакс',
      hide: 'Скрытая',
      priority: 'Приоритетная',
      tags: 'Теги',
      text: 'Добавить первоначальный текст',
      add: 'Добавить'
    },
    actions: {
      settings: 'Настройки страницы',
      addSection: 'Добавить секцию',
      changeFields: 'Изменить поля',
      changeTitle: 'Изменить заголовок',
      changeKind: 'Изменить тип',
      changeAvatar: 'Изменить аватар',
      changeTags: 'Изменить теги',
      changeCategory: 'Изменить категорию',
      changeProperties: 'Изменить свойства',
      hide: {
        on: 'Показать',
        off: 'Скрыть'
      },
      priority: {
        on: 'Снять приоритет',
        off: 'Установить приоритет'
      },
      parallax: {
        on: 'Скрыть параллакс',
        off: 'Показать параллакс'
      },
      delete: 'Удалить',
      deleteItemName: 'страницу'
    },
    changeTitle: {
      header: 'Изменение заголовка',
      text: 'Заголовок страницы',
      change: 'Изменить'
    },
    changeKind: {
      header: 'Изменение типа',
      kind: 'Тип',
      change: 'Изменить'
    },
    changeAvatar: {
      header: 'Изменение аватара',
      avatar: 'Аватар',
      change: 'Изменить аватар',
      delete: 'Удалить аватар',
      serverAvatar: 'Ранее загруженный аватар: {name}',
      noServerAvatar: 'Ранее загруженный аватар отсутствует'
    },
    changeTags: {
      header: 'Изменение тегов',
      tags: 'Теги',
      change: 'Изменить теги'
    }
  },
  section: {
    toPage: 'Перейти на страницу',
    add: 'Добавить секцию',
    change: 'Изменить секцию',
    delete: 'Удалить секцию',
    names: {
      text: 'Текст',
      gallery: 'Фотогалерея',
      files: 'Файлы',
      profiles: 'Профили',
      sliders: 'Слайдер',
      form: 'Форма',
      jupyter: 'Jupyter ноутбук',
      dataset: 'Датасет'
    },
    addSection: 'Добавление секции',
    editSection: 'Редактирование секции',
    loading: 'Загрузка'
  },
  newsFeed: 'Лента новостей',
  components: {
    pageNews: {
      news: 'Новости',
      ads: 'Объявления'
    },
    sectionTextAction: {
      changeText: '@:change',
      delete: '@:delete'
    },
    sectionFiles: {
      mb: 'MБ'
    },
    sectionGallery: {
      images: 'Изображения',
      actions: 'Действия'
    },
    addPage: {
      common: 'Обычная'
    },
    categoryAction: {
      settings: 'Настройки',
      addSubcategory: 'Добавить подкатегорию',
      changeAvatar: 'Изменить аватар',
      changeName: 'Изменить название',
      category: 'категорию',
      delete: '@:delete'
    },
    editCategory: {
      changeCategory: 'Изменение категории',
      parentCategory: 'Родительская категория:',
      change: '@:change'
    },
    pageSections: {
      noSections: 'Нет секций на этой страничке'
    },
    pageSegment: {
      noType: 'Тип {represent} не найден.',
      noPages: 'В разделе <b>{sectionNumber}</b> нет страниц'
    },
    pageView: {
      showOf: '@:shownOf',
      noResults: 'Поиск не дал результатов',
      noPages: 'В этой категории еще нет страничек'
    },
    sectionActions: {
      change: '@:change',
      delete: '@:delete'
    },
    tinymceEditor: {
      error: 'Ошибка загрузки файла',
      uploadFile: 'Загрузить файл',
      uploadButton: 'Загрузка файла',
      name: 'Название файла',
      src: 'Ссылка на файл',
      cancel: 'Закрыть',
      submit: 'Добавить ссылку'
    }
  }
}
