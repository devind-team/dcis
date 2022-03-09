export default {
  index: 'Control Panel',
  support: 'Support',
  groups: 'Group of users',
  permissionFrom: 'Group permissions',
  permissions: 'User permissions',
  usersFile: 'File with users',
  dictionaries: 'Directories',
  dictionary: { profile: 'Profile' },
  ac: {
    name: 'Administration',
    activity: {
      record: 'Record',
      shownOf: '@:shownOf',
      loadMore: '@:loadMore',
      tableHeaders: {
        user: 'User',
        action: 'Action',
        contentType: 'Model',
        objectId: 'Object',
        session: 'System',
        createdAt: 'Event date',
        info: 'Info'
      },
      actions: {
        deleted: 'deleted',
        created: 'created',
        changed: 'edited'
      }
    },
    groups: {
      name: 'Groups',
      change: '@:change',
      deleteGroup: 'Delete group',
      tagged: 'Tagged {count} of {totalCount}',
      tableHeaders: {
        name: '@:name',
        contentType: 'Application/Model',
        codename: 'Permission code'
      }
    },
    history: {
      shownOf: '@:shownOf',
      loadMore: '@:loadMore',
      tableHeaders: {
        user: '@:user',
        page: 'Page',
        browser: 'Browser',
        device: 'Device',
        os: 'Operating system',
        createdAt: 'Event date',
        time: 'Processing time'
      }
    },
    permissions: {
      name: 'Permissions',
      shownOf: '{count} records shown',
      tableHeaders: {
        name: '@:name',
        contentType: 'Application/Модель',
        codename: 'Permission code'
      }
    },
    users: {
      name: 'Users',
      addUsers: 'Add users',
      shownOf: '@:shownOf',
      unloadUsers: 'Unload users',
      tableHeaders: {
        avatar: 'Avatar',
        name: 'Full name',
        username: 'Login',
        email: 'Email',
        groups: 'Groups',
        createdAt: 'Registration'
      },
      changeGroups: {
        header: 'Change groups',
        buttonText: '@:change',
        noGroups: 'No groups selected'
      }
    }
  }
}
