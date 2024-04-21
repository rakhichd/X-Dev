/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}",],
  theme: {
    extend: {
        keyframes: {
            bounce: {
                '0%, 100%': {
                    transform: 'translate(-50%, -50%) translateY(0)',
                },
                '10%, 30%, 50%, 70%, 90%': {
                    transform: 'translate(-50%, -50%) translateY(-50vh)',
                },
                '20%, 40%, 60%, 80%': {
                    transform: 'translate(-50%, -50%) translateX(50vw)',
                },
            },
        },
    },
},
  plugins: [],
}

