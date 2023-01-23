export default {
  name: 'Кураторские группы',
  tableHeaders: {
    name: '@:name',
    group: 'Группа привилегий',
    actions: '@:actions'
  },
  tooltips: {
    changeUsers: 'Изменить пользователей',
    changeOrganizations: 'Изменить организации',
    delete: '@:delete'
  },
  addCuratorGroup: {
    header: 'Добавление кураторской группы',
    name: '@:name',
    group: 'Группа прав',
    buttonText: 'Добавить кураторскую группу'
  },
  deleteCuratorGroup: {
    itemName: 'кураторскую группу',
    delete: '@:delete'
  },
  changeCuratorGroupUsers: {
    header: 'Изменение пользователей',
    successMessage: 'Кураторы добавлены',
    tableHeaders: {
      avatar: 'Аватар',
      name: 'ФИО',
      username: 'Логин',
      email: 'Email',
      actions: '@:actions'
    },
    deleteItemName: 'пользователя',
    deleteTooltip: '@:delete',
    newUsers: 'Новые пользователи',
    buttonText: '@:add'
  },
  changeCuratorGroupOrganizations: {
    header: 'Изменение организаций',
    successMessage: 'Организация добавлена',
    tableHeaders: {
      name: 'Название',
      actions: '@:actions'
    },
    deleteItemName: 'организацию',
    deleteTooltip: '@:delete',
    newOrganizations: 'Новые организации',
    buttonText: '@:add'
  }
}
