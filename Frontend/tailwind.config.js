/** @type {import('tailwindcss').Config} */
export default {
    content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
    theme: {
        extend: {
            fontFamily: {
                // This creates the 'font-poppins' class
                poppins: ["Poppins", "sans-serif"],
            },
            colors: {
                // If you want to use that specific orange from your image:
                brandOrange: "#ff7a1a",
            },
        },
    },
    plugins: [],
};
