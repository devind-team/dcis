import { SidebarConfig } from '@vuepress/theme-default'
import { getSideBar } from './utils'

const path = require('path')

export const sidebarEn: SidebarConfig = {
    '/en/docs/': getSideBar(path.join(`${__dirname}/../../../en/docs`), 'docs'),
    '/en/api/': getSideBar(path.join(`${__dirname}/../../../en/api`), 'api')
}
