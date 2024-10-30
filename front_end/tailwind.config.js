/** @type {import('tailwindcss').Config} */
const defaultTheme = require('tailwindcss/defaultTheme')
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Poppins"', ...defaultTheme.fontFamily.sans]
      },
      colors: {
        white: "#ffffff",
        "custom-darkblue": "#2d3f5d",
        "custom-blue": "#718096",
        "custom-lightblue": "#aab3c0"
      },
      boxShadow: {
        'lg': '4px 4px 6px rgba(113,128,150,0.5)',
      },
      fontSize: {
        'h1': '20px'
      },
      letterSpacing: {
        widest: '3px'
      },
    }
    
  },
  plugins: [],
}

