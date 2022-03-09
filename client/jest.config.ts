import type { InitialOptionsTsJest } from 'ts-jest/dist/types'
const { defaults: jsWithBabel } = require('ts-jest/presets')

const jestConfig: InitialOptionsTsJest = {
  testEnvironment: 'jsdom',
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/$1',
    '^~/(.*)$': '<rootDir>/$1',
    '^vue$': 'vue/dist/vue.common.js'
  },
  moduleFileExtensions: [
    'ts',
    'js',
    'vue',
    'json'
  ],
  transform: {
    ...jsWithBabel.transform,
    '.*\\.(vue)$': 'vue-jest'
  },
  collectCoverage: true,
  collectCoverageFrom: [
    '<rootDir>/components/**/*.vue',
    '<rootDir>/pages/**/*.vue'
  ],
  globals: {
    'vue-jest': {
      pug: { doctype: 'html' }
    },
    'ts-jest': {
      isolatedModules: true
    }
  },
  setupFilesAfterEnv: ['<rootDir>/test/setup.ts']
}

export default jestConfig
