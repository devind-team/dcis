module.exports = {
  content: [
    './components/**/*.{vue,js}',
    './layouts/**/*.vue',
    './pages/**/*.vue',
    './plugins/**/*.{js,ts}',
    './nuxt.config.{js,ts}'
  ],
  darkMode: 'class', // or 'media' or 'class'
  theme: {
    extend: {
      typography: {
        DEFAULT: {
          css: {
            'max-width': 'inherit',
            '.cell': {
              height: '17px',
              width: '17px'
            },
            '.cell:hover': {
              'background-color': '#1b6d85'
            },
            'table td,th': {
              'min-width': '1em',
              border: '2px solid #ced4da',
              padding: '3px 5px',
              'vertical-align': 'top',
              'box-sizing': 'border-box',
              position: 'relative'
            },
            'table > *': {
              'margin-bottom': '0'
            },
            'table .selectedCell:after': {
              'z-index': '2',
              position: 'absolute',
              content: '""',
              left: '0',
              right: '0',
              top: '0',
              bottom: '0',
              background: 'rgba(200, 200, 255, 0.4)',
              'pointer-events': 'none'
            },
            'table .column-resize-handle': {
              position: 'absolute',
              right: '-2px',
              top: '0',
              bottom: '-2px',
              width: '4px',
              'background-color': '#adf',
              'pointer-events': 'none'
            },
            '.resize-cursor': {
              cursor: 'ew-resize'
            },
            img: {
              display: 'initial'
            },
            strong: {
              color: 'inherit'
            },
            a: {
              color: '#1976d2'
            },
            'h1, h2, h3, h4, h5': {
              color: 'inherit'
            },
            '.iframe-wrapper': {
              'align-items': 'center',
              display: 'flex',
              'justify-content': 'center'
            }
          }
        },
        lg: {
          css: {
            'ol > li': {
              'padding-left': '3em'
            }
          }
        }
      }
    }
  },
  variants: {
    extend: {}
  },
  plugins: [
    require('@tailwindcss/typography')
  ],
  important: true
}
