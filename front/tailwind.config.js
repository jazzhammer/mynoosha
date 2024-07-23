/** @type {import('tailwindcss').Config} */
import flowbitePlugin from 'flowbite/plugin'
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        myhigh_white: '#f2f1ed',
        mymid_white: '#e2d2b1',
        mylow_white: '#b2aea9',
        myroon: {
          100: '#ee386b',
          500: '#a92d4f',
          900: '#621a2d',
        },
        mywood: {
          100: '#d78058',
          500: '#834a45',
          900: '#432d2b',
        },
        myblue: {
          50: '#d2dbf1',
          100: '#5ba1f1',
          500: '#477fbb',
          900: '#31577e',
        },
        primary: {
          50: '#FFF5F2',
          100: '#FFF1EE',
          200: '#FFE4DE',
          300: '#FFD5CC',
          400: '#FFBCAD',
          500: '#FE795D',
          600: '#EF562F',
          700: '#EB4F27',
          800: '#CC4522',
          900: '#A5371B'
        }
      }
    },
  },
  plugins: [flowbitePlugin],
}

