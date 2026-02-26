/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bg: {
          DEFAULT: '#0A0A0A',
          card: '#FFFFFF',
          hover: '#F8F8F8',
          muted: '#1A1A1A',
        },
        accent: {
          gold: { light: '#FDF6E3', DEFAULT: '#D4A843', dark: '#8B6914' },
          purple: { light: '#F3EEFF', DEFAULT: '#7C6DB0', dark: '#4A3D6B' },
          teal: { light: '#E6F9F5', DEFAULT: '#3D9B8F', dark: '#1F5C54' },
          pink: { light: '#FFF0F3', DEFAULT: '#C27185', dark: '#7A3A4A' },
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
      boxShadow: {
        card: '0 2px 20px rgba(0, 0, 0, 0.08)',
        'card-hover': '0 8px 30px rgba(0, 0, 0, 0.12)',
      },
    },
  },
  plugins: [],
}
