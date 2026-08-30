/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        skyguard: {
          dark: '#030712',
          navy: '#060d24',
          card: '#0a1638',
          cardBorder: '#1e3875',
          accent: '#00a8ff',
          neon: '#00f0ff',
          glow: 'rgba(0, 168, 255, 0.4)',
        }
      },
      boxShadow: {
        'neon-blue': '0 0 20px rgba(0, 168, 255, 0.4), inset 0 0 15px rgba(0, 168, 255, 0.1)',
        'neon-glow': '0 0 35px rgba(0, 240, 255, 0.35)',
        'btn-glow': '0 0 25px rgba(0, 168, 255, 0.6)',
        'card-glow': '0 0 25px rgba(10, 22, 56, 0.8), 0 0 1px rgba(0, 168, 255, 0.3)',
      },
      animation: {
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'spin-slow': 'spin 20s linear infinite',
        'spin-reverse-slow': 'spin-reverse 25s linear infinite',
        'float': 'float 6s ease-in-out infinite',
        'float-delayed': 'float 6s ease-in-out 3s infinite',
        'beam': 'beam 3s ease-in-out infinite',
      },
      keyframes: {
        'spin-reverse': {
          '0%': { transform: 'rotate(360deg)' },
          '100%': { transform: 'rotate(0deg)' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        beam: {
          '0%, 100%': { opacity: '0.2', transform: 'scaleY(0.95)' },
          '50%': { opacity: '0.8', transform: 'scaleY(1.05)' },
        }
      }
    },
  },
  plugins: [],
}
