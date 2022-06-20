import type { SidebarConfig } from '@vuepress/theme-default'

export const sidebarEn: SidebarConfig = {
    '/guide/': [
        {
            text: 'Guide',
            children: [
                '/en/guide/README.md'
            ]
        }
    ],
    '/section1/': [
        {
            text: 'Section1',
            children: [
                '/en/section1/sec1.md',
                '/en/section1/sec2.md'
            ]
        }
    ],
    '/section2/': [
        {
            text: 'Section2',
            collapsible: true,
            children: [
                '/en/section2/sec1.md',
                '/en/section2/sec2.md'
            ]
        }
    ]
}