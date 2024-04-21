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
                '25%': {
                    transform: 'translate(-50%, -50%) translateY(-50vh)',
                },
                '50%': {
                    transform: 'translate(-50%, -50%) translateX(50vw)',
                },
                '75%': {
                    transform: 'translate(-50%, -50%) translateY(50vh)',
                },
            },
            'bounce-reverse': {
                '0%, 100%': {
                    transform: 'translate(-50%, -50%) translateY(0)',
                },
                '25%': {
                    transform: 'translate(-50%, -50%) translateY(50vh)',
                },
                '50%': {
                    transform: 'translate(-50%, -50%) translateX(-50vw)',
                },
                '75%': {
                    transform: 'translate(-50%, -50%) translateY(-50vh)',
                },
            },
        },
    },
},
  plugins: [],
}

