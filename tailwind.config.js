/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ['./index.html'],
    theme: {
        extend: {
            colors: {
                'oes-primary': 'var(--color-primary)',
                'oes-secondary': 'var(--color-secondary)',
                'oes-blue': 'var(--color-oes-blue)',
                'oes-yellow': 'var(--color-oes-yellow)',
                'oes-white-point': 'var(--color-oes-white)',
                'oes-green': 'var(--color-oes-green)',
                'oes-red': 'var(--color-oes-red)',
            },
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
                serif: ['ui-serif', 'Georgia'],
            },
        },
    },
    plugins: [],
};
