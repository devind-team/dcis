export default {
  dcis: '@:dcis.home',
  name: 'Справочники',
  search: '@:search',
  totalCount: '@:totalCount',
  shownOf: '@:shownOf',
  loadMore: '@:loadMore',
  yes: '@:yes',
  no: '@:no',
  privileges: {
    header: 'Привилегии',
    tableHeaders: {
      id: '@:id',
      name: '@:name',
      key: 'Ключ',
      createdAt: 'Дата создания'
    }
  },
  organizations: {
    header: 'Организации',
    tableHeaders: {
      id: '@:id',
      name: '@:name',
      createdAt: 'Дата создания'
    }
  },
  departments: {
    header: 'Департаменты',
    tableHeaders: {
      id: '@:id',
      name: '@:name',
      code: 'Код',
      createdAt: 'Дата создания'
    }
  }
}
