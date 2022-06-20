import type { NavbarConfig } from '@vuepress/theme-default'

export const navbarRu: NavbarConfig = [
    {
        text: 'Docs',
        link: '/docs/',
        children: [
            '/docs/sec1.md'
        ]
    },
    {
        text: 'API',
        link: '/api/',
        children: [
            {
                text: 'Секция1',
                children: [
                    '/api/sec1.md',
                    '/api/sec2.md'
                ]
            }
        ]
    }
]