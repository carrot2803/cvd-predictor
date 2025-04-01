document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    form.addEventListener("submit", async function (event) {
        event.preventDefault(); // Prevent default form submission

        let formData = new FormData(form);
        let data = {};

        // Convert FormData to a regular object
        formData.forEach((value, key) => {
            data[key] = value;
        });

        const numericalFields = [
            "Sex", "GeneralHealth", "PhysicalHealthDays", "MentalHealthDays",
            "LastCheckupTime", "MentalHealthDays", "HadDiabetes"
        ];
        numericalFields.forEach(field => data[field] = parseInt(data[field], 10));

        // Convert Yes/No responses to boolean (1/0)
        const booleanFields = [
            "PhysicalActivities", "HadAsthma", "HadSkinCancer", "HadCOPD",
            "HadDepressiveDisorder", "HadKidneyDisease", "HadArthritis",
            "HaveHighCholesterol", "SensoryImpairments", "Vaccinated"
        ];
        booleanFields.forEach(field => {
            if (data[field] === "Yes") data[field] = 1;
            else if (data[field] === "No") data[field] = 0;
        });


        let feet = parseInt(data["HeightFeet"], 10);
        let inches = parseInt(data["HeightInches"], 10);
        data["HeightInMeters"] = ((feet * 12) + inches) * 0.0254; // 1 inch = 0.0254 meters
        delete data["HeightFeet"];
        delete data["HeightInches"];

        // Convert Weight (lbs) to Kilograms
        let pounds = parseFloat(data["WeightPounds"]);
        data["WeightInKilograms"] = pounds * 0.453592; // 1 lb = 0.453592 kg
        delete data["WeightPounds"];


        console.log("Cleaned Data:", data); // Debugging

        // Send Data via Fetch API
        try {
            const response = await fetch("/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                const result = await response.json();
                console.log("Response from server:", result);
                window.location.href = "/results";
                alert("Survey submitted successfully!");
            } else {
                alert("Failed to submit survey. Please try again.");
            }
        } catch (error) {
            console.error("Error submitting form:", error);
            alert("An error occurred. Please check your internet connection.");
        }
    });
});
