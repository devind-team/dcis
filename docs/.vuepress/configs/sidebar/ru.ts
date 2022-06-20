import type { SidebarConfig } from '@vuepress/theme-default'

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
            text: 'API',
            collapsible: true,
            children: [
                '/api/sec1.md',
                '/api/sec2.md'
            ]
        }
    ]
}