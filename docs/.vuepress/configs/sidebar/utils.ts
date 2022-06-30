import { SidebarConfigArray } from '@vuepress/theme-default'

const fs = require('fs')
const path = require('path')

export function getSideBar(dir: string, root: string): SidebarConfigArray {
    const sideBarArray: SidebarConfigArray = []
    for (const entry of fs.readdirSync(dir)) {
        const entryPath = path.join(dir, entry)
        const stats = fs.lstatSync(entryPath)
        if (stats.isDirectory()) {
            sideBarArray.push({
                text: entry,
                children: getSideBar(entryPath, root)
            })
        } else if (stats.isFile()) {
            if (!entry.match(/readme\.md/i)) {
                const splitEntry = entryPath.split(path.sep)
                sideBarArray.push(
                    `/${splitEntry.slice(splitEntry.lastIndexOf(root)).join('/')}`
                )
            }
        }
    }
    return sideBarArray
}
