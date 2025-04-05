export const translations = {
    en: {
        hero: {
            title: ({vendor}) => `${vendor} Meal Planner`,
            subtitle: () => "Plan, Eat, Be Fit!",
        },
        requestForm: {
            setYourGoals: () => "Set Your Nutritional Goals",
            setYourGoalSub: () => "Give us the requirements, we give you the plan!",
            kitchen: () => "Kitchen",
            generateMeal: () => "Generate Meal Plan",
            optional: () => "Optional",
            selectDate: () => "Select Date",
            dislikedFoods: () => "Disliked Foods",
            canFoodRepeat: () => "Can a Food Repeat",
            typeFoodEnter: () => "Type a food and press Enter",
        },
        macro: {
            calories: () => "Calories",
            protein: () => "Protein",
            carb: () => "Carb",
            carbohydrate: () => "Carbohydrate",
            fat: () => "Fat",
        },
        mealPlan: {
            yourMealPlan: () => "Your Meal Plan",
            orderTheseFoods: () => `Order these from`,
            items: () => "items",
            dontLike: () => "Don't Like",
        },

    },
    hu: {
        hero: {
            title: ({vendor}) => `${vendor} Étrend Tervező`,
            subtitle: () => "Tervezz, Zabálj, Be Fit!",
        },
        requestForm: {
            setYourGoals: () => "Állítsd be a tápanyag céljaidat",
            setYourGoalSub: () => "Add meg a céljaidat, mi pedig elkészítjük a napi étrendedet!",
            kitchen: () => "Konyha",
            generateMeal: () => "Étrend generálása",
            optional: () => "Opcionális",
            selectDate: () => "Válassz dátumot",
            dislikedFoods: () => "Nem kedvelt ételek",
            canFoodRepeat: () => "Ismétlődhet étel",
            typeFoodEnter: () => "Írj be egy ételt és nyomj Enter-t",
        },
        macro: {
            calories: () => "Kalória",
            protein: () => "Fehérje",
            carb: () => "Szénhidrát",
            carbohydrate: () => "Szénhidrát",
            fat: () => "Zsír",
        },
        mealPlan: {
            yourMealPlan: () => "A te étrended",
            orderTheseFoods: () => `Rendeld meg ezeket innen:`,
            items: () => "étel",
            dontLike: () => "Nem szeretem",
        },

    },
};
