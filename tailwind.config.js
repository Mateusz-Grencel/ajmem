module.exports = {
  content: [
    './templates/**/*.html',
    './static/js/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        'red-rose': '#e04258',  // Twój własny kolor
        'light-rose': '#FFD6E4',
        'turquoise':'#06D6A0',
      },
      width: {
        '3/5': '60%',
        '1/6': '16%',
      }
    },
  },
  plugins: [],
}