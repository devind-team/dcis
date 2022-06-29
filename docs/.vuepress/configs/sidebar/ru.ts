import type { SidebarConfig } from '@vuepress/theme-default'

// const fs = require('fs')
// const path = require('path')
//
// function getSideBar(folder, text) {
//     const extension = ['.md']
//     const files = fs.
//     readdirSync(path.join(`${__dirname}/../${folder}`)).
//     filter(
//         (item) =>
//             item.toLowerCase() != 'readme.md' &&
//             fs.statSync(path.join(`${__dirname}/../${folder}`, item)).isFile() &&
//         extension.includes(path.extname(item))
//     )
//     return [{text: text, children: ['', ...files]}]
// }


export const sidebarRu: SidebarConfig = {
    '/docs/': [
        {
            text: 'Docs',
            children: [
                '/docs/README.md'
            ]
        }
    ],
    '/api/': [
        {
            text: 'core',
            collapsible: true,
            children: [
                '/api/apps/core/models.md',
                '/api/apps/core/apps.md',
                '/api/apps/core/signals.md',
                '/api/apps/core/middleware/database_requests_middleware.md',
                '/api/apps/core/schema/mutations.md',
                '/api/apps/core/schema/types.md',
                '/api/apps/core/services/user_services.md'
            ]
        },
        {
            text: 'dashboard',
            collapsible: true,
            children: [
                '/api/apps/dashboard/apps.md',
                '/api/apps/dashboard/schema/types.md'
            ]
        },
        {
            text: 'dcis',
            collapsible: true,
            children: [
                '/api/apps/dcis/admin.md',
                '/api/apps/dcis/apps.md',
                '/api/apps/dcis/validators.md',
                '/api/apps/dcis/views.md',
                '/api/apps/dcis/helpers/divisions.md',
                '/api/apps/dcis/helpers/info_fields.md',
                '/api/apps/dcis/helpers/mutation.md',
                '/api/apps/dcis/helpers/theme_to_rgb.md',
                '/api/apps/dcis/models/document.md',
                '/api/apps/dcis/models/privilege.md',
                '/api/apps/dcis/models/project.md',
                '/api/apps/dcis/models/sheet.md',
                '/api/apps/dcis/permissions/document_permissions.md',
                '/api/apps/dcis/permissions/period_permissions.md',
                '/api/apps/dcis/permissions/project_permissions.md',
                '/api/apps/dcis/permissions/sheet_permissions.md',
                '/api/apps/dcis/permissions/value_permissions.md',
                // '/api/apps/dcis/schema/',
            ]
        },
        {
            text: 'notification',
            collapsible: true,
            children: [
                '/api/apps/notification/readme.md'
            ]
        },
        {
            text: 'pages',
            collapsible: true,
            children: [
                '/api/apps/pages/apps.md',
                '/api/apps/pages/decorators.md',
                '/api/apps/pages/signals.md',
                '/api/apps/pages/tests.md',
                '/api/apps/pages/validators.md',
            ]
        },

    ]
}