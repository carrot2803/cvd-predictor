document.addEventListener("DOMContentLoaded", function () {
    const styleClasses = {
        "numeric-options": "appearance-none border-2 rounded-md w-full py-2 px-3 text-gray-700 text-sm focus:outline-none",
        "selection-options": "appearance-none border-2 rounded-md w-full py-2 px-3 text-gray-700 text-sm focus:outline-none",
        "yes-no-question": "mb-4 flex flex-col sm:flex-row sm:items-center justify-between sm:space-x-3",
        "yes-no-question-label": "block text-gray-700 text-sm mb-2 sm:mb-0 w-full text-left sm:w-4/5",
        "yes-no-container": "flex gap-4 sm:w-1/5",
        "yes-no-option": "w-full py-1 text-gray-700 px-3 border-2 border-gray-200 text-sm rounded-md text-center font-medium cursor-pointer peer-checked:bg-blue-600 peer-checked:text-white peer-checked:border-blue-600 hover:bg-blue-600 hover:text-white hover:border-blue-600",
        "section-label": "text-md font-bold text-blue-600 mb-4",
        "multi-question-row": "flex flex-col md:flex-row md:space-x-4",
        "general-question-label": "block text-gray-700 text-sm mb-2",
        "back-btn": "back-btn bg-white text-gray-700 border-2 border-blue-600 hover:bg-blue-600 hover:text-white font-bold py-1 px-4 rounded-md focus:outline-none focus:shadow-outline",
        "next-btn": "text-gray-700 bg-blue-600 border-2 border-blue-600 text-white hover:bg-blue-800 hover:border-blue-800 font-bold py-1 px-4 rounded-md focus:outline-none focus:shadow-outline",
        "submit-btn": "text-gray-700 bg-blue-600 border-2 border-blue-600 text-white hover:bg-blue-800 hover:border-blue-800 font-bold py-1 px-4 rounded-md focus:outline-none focus:shadow-outline",
        "nav-btn": "flex items-center w-1/3",
        "nav-next-btn": "flex items-center justify-end w-1/3",
        "navigation-section": "flex justify-between mt-8 text-sm",
        "status-bar": "text-gray-700 flex items-center justify-center w-1/3",
    };

    function applyStyles() {
        Object.entries(styleClasses).forEach(([className, styles]) => {
            document.querySelectorAll(`.${className}`).forEach(el => {
                el.className = `${className} ${styles}`;
            });
        });
    }

    applyStyles();
    window.addEventListener("popstate", applyStyles);
});