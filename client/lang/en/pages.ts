export default {
  index: 'Pages',
  categories: 'Categories',
  category: {
    addCardHeader: 'Add category',
    addDialog: {
      header: 'Add category',
      parentCategory: 'Parent category',
      avatar: 'Avatar',
      text: 'Name of category',
      add: '@:add'
    },
    position: 'Sort order',
    parentId: 'Parent category',
    noCategories: 'No categories yet'
  },
  page: {
    addCardHeader: 'Add page',
    add: {
      header: 'Add page',
      category: 'Category',
      avatar: 'Avatar',
      title: 'Title',
      kind: 'Type',
      parallax: 'Parallax',
      hide: 'Hidden',
      priority: 'Priority',
      tags: 'Tags',
      text: 'Add original text',
      add: '@:add'
    },
    actions: {
      settings: 'Page settings',
      addSection: 'Add section',
      changeFields: 'Change fields',
      changeTitle: 'Change title',
      changeKind: 'Change type',
      changeAvatar: 'Change avatar',
      changeTags: 'Change tags',
      changeCategory: 'Change category',
      changeProperties: 'Change properties',
      hide: {
        on: 'Show',
        off: 'Hide'
      },
      priority: {
        on: 'Remove priority',
        off: 'Set priority'
      },
      parallax: {
        on: 'Hide parallax',
        off: 'Show parallax'
      },
      delete: '@:delete',
      deleteItemName: 'page'
    },
    changeTitle: {
      header: 'Edit title',
      text: 'Page title',
      change: '@:change'
    },
    changeKind: {
      header: 'Edit type',
      kind: 'Type',
      change: '@:change'
    },
    changeAvatar: {
      header: 'Edit avatar',
      avatar: 'Avatar',
      change: 'Edit avatar',
      delete: 'Delete avatar',
      serverAvatar: 'Previously uploaded avatar: {name}',
      noServerAvatar: 'Previously uploaded avatar is missing'
    },
    changeTags: {
      header: 'Edit tags',
      tags: 'Tags',
      change: 'Edit tags'
    }
  },
  section: {
    toPage: 'Go to page',
    add: 'Add section',
    change: 'Change section',
    delete: 'Delete section',
    names: {
      text: 'Text',
      gallery: 'Gallery',
      files: 'Files',
      profiles: 'Profiles',
      sliders: 'Sliders',
      form: 'Form',
      jupyter: 'Jupyter Notebook',
      dataset: 'Dataset'
    },
    addSection: 'Add section',
    editSection: 'Edit section',
    loading: '@:loading'
  },
  newsFeed: 'News feed',
  components: {
    pageNews: {
      news: 'News',
      ads: 'Announcement'
    },
    sectionTextAction: {
      changeText: 'Edit text',
      delete: '@:delete'
    },
    sectionFiles: {
      mb: 'MB'
    },
    addPage: {
      common: 'Regular'
    },
    categoryAction: {
      settings: 'Settings',
      addSubcategory: 'Add subcategory',
      changeAvatar: 'Edit avatar',
      changeName: 'Edit name',
      category: 'category',
      delete: '@:delete'
    },
    editCategory: {
      changeCategory: 'Edit category',
      parentCategory: 'Parent category:',
      change: '@:change'
    },
    pageSections: {
      noSections: 'No sections on this page'
    },
    pageSegment: {
      noType: 'No type {represent} found.',
      noPages: 'No pages in section <b>{sectionNumber}</b>'
    },
    pageView: {
      shownOf: '@:shownOf',
      noResults: 'No results found',
      noPages: 'No pages in this category'
    },
    sectionActions: {
      change: '@:change',
      delete: '@:delete'
    },
    tinymceEditor: {
      error: 'File upload error',
      uploadFile: 'Upload file',
      uploadButton: 'Uploading file',
      name: 'File name',
      src: 'Link to file',
      cancel: 'Close',
      submit: 'Add link'
    }
  }
}
