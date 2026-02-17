/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts}'],
  theme: {
    extend: {
      colors: {
        cream: '#FFF8F0',
        parchment: '#F5EDE0',
        terracotta: '#C45D3E',
        'terracotta-dark': '#A34830',
        sage: '#7A8B69',
        'sage-light': '#A3B592',
        ink: '#2D1B0E',
        'ink-light': '#5C4A3A',
      },
      fontFamily: {
        display: ['"DM Serif Display"', 'Georgia', 'serif'],
        body: ['"Space Grotesk"', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        'warm': '0 2px 15px -3px rgba(45, 27, 14, 0.08), 0 4px 6px -4px rgba(45, 27, 14, 0.05)',
        'warm-lg': '0 10px 30px -5px rgba(45, 27, 14, 0.12), 0 8px 10px -6px rgba(45, 27, 14, 0.06)',
      },
    },
  },
  plugins: [],
}
