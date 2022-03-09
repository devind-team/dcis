module.exports = {
  root: true,
  env: {
    browser: true,
    node: true
  },
  extends: [
    '@nuxtjs/eslint-config-typescript',
    'plugin:nuxt/recommended'
  ],
  plugins: ['import'],
  // add your custom rules here
  rules: {},
  settings: {
    'import/parsers': {
      '@typescript-eslint/parser': ['.ts', '.tsx']
    },
    'import/resolver': {
      typescript: './tsconfig.json'
    }
  },
  overrides: [{
    files: ['**/*.d.ts'],
    rules: {
      'no-unused-vars': 'off',
      '@typescript-eslint/no-unused-vars': 'off',
      'no-use-before-define': 'off',
      '@typescript-eslint/no-use-before-define': 'off'
    }
  },
  {
    files: ['**/*.vue'],
    rules: {
      'no-use-before-define': 'off',
      '@typescript-eslint/no-use-before-define': 'off',
      'vue/multi-word-component-names': 'off'
    }
  },
  {
    files: ['**/*.ts'],
    rules: {
      'no-undef': 'off',
      'import/no-mutable-exports': 'off'
    }
  },
  {
    files: ['**/graphql.d.ts'],
    rules: {
      camelcase: 'off'
    }
  }]
}
