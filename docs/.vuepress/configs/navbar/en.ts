import type { NavbarConfig } from '@vuepress/theme-default'

export const navbarEn: NavbarConfig = [
    {
        text: 'Docs',
        link: '/en/docs/'
    },
    {
        text: 'API',
        children: [
            {
                text: 'section1',
                children: [
                    '/en/api/sec1.md',
                    '/en/api/sec2.md'
                ]
            }
        ]
    }
]