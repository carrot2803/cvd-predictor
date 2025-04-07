document.addEventListener("DOMContentLoaded", function () {
    const forms = document.querySelectorAll('.survey-page');

    function computeGeneralHealthScore(data) {
        let score = 4;
        const normalizedHadAsthma = (data.HadAsthma === 1) ? 1 : 0;
        const normalizedHadDiabetes = [1, 2].includes(data.HadDiabetes) ? 1 : 0;
        const chronicConditions = [
            normalizedHadAsthma,
            data.HadSkinCancer || 0,
            data.HadCOPD || 0,
            data.HadKidneyDisease || 0,
            data.HadArthritis || 0,
            normalizedHadDiabetes,
            data.HadDepressiveDisorder || 0
        ];
        const chronicCount = chronicConditions.reduce((sum, val) => sum + val, 0);

        // Apply penalty logic
        if (data.PhysicalHealthDays > 20 || data.MentalHealthDays > 20) score -= 1;
        if (data.PhysicalHealthDays > 27 || data.MentalHealthDays > 27) score -= 1;
        if (chronicCount >= 2) score -= 1;
        if (chronicCount >= 4) score -= 1;
        if (data.SmokerStatus >= 2 || data.AlcoholDrinkers === 1) score -= 1;
        if (!data.PhysicalActivities) score -= 1;
        if (data.BMI < 18.5 || data.BMI >= 30) score -= 1;
        if (data["Sensory Impairments"] === 1 || data["Mobility"] === 1) score -= 1;

        return Math.max(1, Math.min(4, score));
    }


    forms.forEach(form => {
        form.addEventListener("submit", async function (event) {
            event.preventDefault();
            const currentPage = parseInt(this.id.replace("page-", ""));
            if (currentPage != forms.length) {
                navigateToPage(currentPage + 1);
                return;
            }

            let data = {};

            forms.forEach(form => {
                const pageFormData = new FormData(form);
                pageFormData.forEach((value, key) => {
                    data[key] = value;
                });
            });

            // Convert necessary fields to numbers
            const numericalFields = [
                "Sex", "PhysicalHealthDays", "MentalHealthDays", "HadAsthma",
                "LastCheckupTime", "HadDiabetes", "SmokerStatus", "AgeCategory", "AlcoholDrinkers"
            ];
            numericalFields.forEach(field => data[field] = parseInt(data[field], 10));

            let age = parseInt(data["AgeCategory"], 10);
            if (age >= 80)
                data["AgeCategory"] = 13
            else
                data["AgeCategory"] = Math.floor((age - 18) / 5) + 1;


            // Convert Height to Meters
            let feet = parseInt(data["HeightFeet"], 10);
            let inches = parseInt(data["HeightInches"], 10);
            data["HeightInMeters"] = ((feet * 12) + inches) * 0.0254; // Convert height to meters
            delete data["HeightFeet"];
            delete data["HeightInches"];

            // Convert Weight (lbs) to Kilograms
            let pounds = parseFloat(data["WeightPounds"]);
            data["WeightInKilograms"] = pounds * 0.453592; // Convert weight to kg
            delete data["WeightPounds"];

            // Calculate BMI
            data["BMI"] = data["WeightInKilograms"] / (data["HeightInMeters"] ** 2);
            data["HadDepressiveDisorder"] = data["MentalHealthDays"] > 25 ? 1 : 0;
            // Convert Yes/No fields to 1/0
            const booleanFields = [
                "PhysicalActivities", "HadSkinCancer", "HadCOPD",
                "HadKidneyDisease", "HadArthritis", "HaveHighCholesterol",
                "Sensory Impairments", "Vaccinated"
            ];

            booleanFields.forEach(field => {
                if (data[field] === "Yes") data[field] = 1;
                else if (data[field] === "No") data[field] = 0;
            });

            data["Mobility"] = data["Mobility"] === "1" ? 1 : 0;
            data["GeneralHealth"] = computeGeneralHealthScore(data)

            // Define the order of keys
            const orderedKeys = [
                "Sex", "GeneralHealth", "PhysicalHealthDays", "MentalHealthDays",
                "LastCheckupTime", "PhysicalActivities", "HadAsthma", "HadSkinCancer",
                "HadCOPD", "HadDepressiveDisorder", "HadKidneyDisease", "HadArthritis",
                "HadDiabetes", "SmokerStatus", "AgeCategory", "HeightInMeters",
                "WeightInKilograms", "BMI", "AlcoholDrinkers", "HaveHighCholesterol",
                "Sensory Impairments", "Vaccinated", "Mobility"
            ];

            let orderedData = {};
            orderedKeys.forEach(key => {
                if (key in data) {
                    orderedData[key] = data[key];
                }
            });

            console.log("Ordered Data:", orderedData); // Debugging

            try {
                const response = await fetch("/predict", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(orderedData)
                });

                if (response.ok) {
                    const result = await response.json();
                    console.log("Response from server:", result);

                    sessionStorage.setItem("surveyResult", result.message);
                    window.location.href = "/results";
                } else {
                    alert("Failed to submit survey. Please try again.");
                }
            } catch (error) {
                console.error("Error submitting form:", error);
                alert("An error occurred. Please check your internet connection.");
            }
        });
    });


    document.querySelectorAll(".back-btn").forEach(button => {
        button.addEventListener("click", function () {
            const currentForm = this.closest(".survey-page");
            const currentPage = parseInt(currentForm.id.replace("page-", ""));
            navigateToPage(currentPage - 1);
        });
    });

    function navigateToPage(pageNum) {
        document.querySelectorAll(".survey-page").forEach(form => {
            form.classList.add("hidden");
        });
        const form = document.getElementById(`page-${pageNum}`);
        form.classList.remove("hidden");
        window.scrollTo({ top: 0, behavior: "smooth" });
    }

    if (document.getElementById("healthSurveyForm")) {
        navigateToPage(1);
    }
});
