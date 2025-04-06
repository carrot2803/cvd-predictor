document.addEventListener("DOMContentLoaded", function () {
    const styleClasses = {
        "numeric-options": "appearance-none border-2 rounded-lg w-full py-2 px-3 text-gray-700 focus:outline-none",
        "selection-options": "appearance-none border-2 rounded-lg w-full py-2 px-3 text-gray-700 focus:outline-none",
        "yes-no-question": "mb-4 flex flex-col sm:flex-row sm:items-center justify-between sm:space-x-3",
        "yes-no-question-label": "block text-gray-700 text-md mb-2 sm:mb-0 w-full text-left sm:w-2/3",
        "yes-no-container": "flex gap-4 sm:w-1/3",
        "yes-no-option": "w-full py-1 px-3 border-2 border-gray-200 rounded-lg text-center font-medium cursor-pointer peer-checked:bg-sky-500 peer-checked:text-white peer-checked:border-sky-500 hover:bg-sky-500 hover:text-white hover:border-sky-500",
        "section-label": "text-md font-bold text-sky-500 mb-4",
        "multi-question-row": "flex flex-col md:flex-row md:space-x-4",
        "general-question-label": "block text-gray-700 text-md mb-2",
        "general-question-bold-label": "block text-gray-700 text-md font-bold mb-2",
    };

    function applyStyles() {
        document.querySelectorAll(".section-label").forEach(el => {
            el.className = styleClasses["section-label"];
        });

        document.querySelectorAll(".general-question-label").forEach(el => {
            el.className = styleClasses["general-question-label"];
        });

        document.querySelectorAll(".general-question-bold-label").forEach(el => {
            el.className = styleClasses["general-question-bold-label"];
        });

        document.querySelectorAll(".multi-question-row").forEach(el => {
            el.className = styleClasses["multi-question-row"];
        });

        document.querySelectorAll(".selection-options").forEach(el => {
            el.className = styleClasses["selection-options"];
        });

        document.querySelectorAll(".numeric-options").forEach(el => {
            el.className = styleClasses["numeric-options"];
        });

        document.querySelectorAll(".yes-no-question").forEach(el => {
            el.className = styleClasses["yes-no-question"];
        });

        document.querySelectorAll(".yes-no-container").forEach(el => {
            el.className = styleClasses["yes-no-container"];
        });

        document.querySelectorAll(".yes-no-option").forEach(el => {
            el.className = styleClasses["yes-no-option"];
        });

        document.querySelectorAll(".yes-no-question-label").forEach(el => {
            el.className = styleClasses["yes-no-question-label"];
        });
    }

    applyStyles();
    window.addEventListener("popstate", applyStyles);
});