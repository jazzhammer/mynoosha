/** @type {import('tailwindcss').Config} */
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
        }
      }
    },
  },
  plugins: [],
}

