import { SidebarConfig } from '@vuepress/theme-default'
import { getSideBar } from './utils'

const path = require('path')

export const sidebarRu: SidebarConfig = {
    '/docs/': getSideBar(path.join(`${__dirname}/../../../docs`), 'docs'),
    '/api/': getSideBar(path.join(`${__dirname}/../../../api`), 'api')
}
