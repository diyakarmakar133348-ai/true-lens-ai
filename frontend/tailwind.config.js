/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: '#0a0e1a',
        'dark-card': '#12182b',
        cyan: '#00d4ff',
        'cyan-dark': '#0099cc',
        'red-accent': '#ff4d6d',
        'green-accent': '#00c9a7',
      }
    },
  },
  plugins: [],
}