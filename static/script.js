document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");

    form.addEventListener("submit", async function (event) {
        event.preventDefault(); // Prevent default form submission

        let formData = new FormData(form);
        let data = {};

        formData.forEach((value, key) => {
            data[key] = value;
        });

        // Convert necessary fields to numbers
        const numericalFields = [
            "Sex", "GeneralHealth", "PhysicalHealthDays", "MentalHealthDays",
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

        // Convert Yes/No fields to 1/0
        const booleanFields = [
            "PhysicalActivities", "HadAsthma", "HadSkinCancer", "HadCOPD",
            "HadDepressiveDisorder", "HadKidneyDisease", "HadArthritis",
            "HaveHighCholesterol", "Sensory Impairments", "Vaccinated"
        ];
        booleanFields.forEach(field => {
            if (data[field] === "Yes") data[field] = 1;
            else if (data[field] === "No") data[field] = 0;
        });

        data["Mobility"] = data["Mobility"] === "1" ? 1 : 0;

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

    const generalHealthSection = document.getElementById("generalHealth");
    const lifestyleSection = document.getElementById("lifestyle");
    const medicalHistorySection = document.getElementById("medicalHistory");
    const generalHealthNextButton = generalHealthSection.querySelector(".next-btn");
    const lifestyleBackButton = lifestyleSection.querySelector(".back-btn");
    const lifestyleNextButton = lifestyleSection.querySelector(".next-btn");
    const medicalHistoryBackButton = medicalHistorySection.querySelector(".back-btn");

    generalHealthSection.style.display = "block";
    lifestyleSection.style.display = "none";
    medicalHistorySection.style.display = "none";

    generalHealthNextButton.addEventListener("click", function () {
        lifestyleSection.style.display = "block";
        generalHealthSection.style.display = "none";
        window.scrollTo({ top: 0, behavior: "smooth" });
    });

    lifestyleBackButton.addEventListener("click", function () {
        generalHealthSection.style.display = "block";
        lifestyleSection.style.display = "none";
        window.scrollTo({ top: 0, behavior: "smooth" });
    });

    lifestyleNextButton.addEventListener("click", function () {
        medicalHistorySection.style.display = "block";
        lifestyleSection.style.display = "none";
        window.scrollTo({ top: 0, behavior: "smooth" });
    });

    medicalHistoryBackButton.addEventListener("click", function () {
        lifestyleSection.style.display = "block";
        medicalHistorySection.style.display = "none";
        window.scrollTo({ top: 0, behavior: "smooth" });
    });
});
