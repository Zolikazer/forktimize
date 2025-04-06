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
            caloriesSmall: () => "calories",
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
        feedback: {
            ready: () => "Your meal plan is ready.",
            inProgress: () => "Generating your meal plan... Please wait!",
            failed: () => `Sorry, we could not find a meal plan that meets your needs. 😔 <strong>Adjust your input and try again!</strong>`,
            notStarted: () => `No meal plan generated yet. Click <strong>"Generate Meal Plan"</strong> to get started!`,
        },
        instructions: {
            needHelp: () => "Need help?",
            addGoals: () => "Add your <strong>nutritional goals</strong> (calories, protein, carbs, fats).",
            enterMinMax: () => "You only need to enter either the <strong>minimum or maximum</strong> values.",
            selectDay: () => "<strong>Select a day</strong> for which you want to order.",
            appGenerate: () => "The app will generate a <strong>meal plan</strong> that fit your requirements.",
            addDislikedFood: () => 'If you have foods you dislike, <strong>add them to the "Foods You dislike" field</strong> to filter them out.',
            minimizePrice: () => "The <strong>generator prioritizes minimizing price</strong> while still fitting your nutritional constraints.",
            lessConstraintBetter: () => "The <strong>more constraints you add, the harder it is</strong> to find a cheap meal plan"
        },
        summary: {
            title: () => "Your Meal Plan Summary",
            macroRatio: () => "Macronutrient Ratio",
        },
        foodLog: {
            title: () => "Macro Equivalents",
            subtitle: () => "Trackable Format",
            mfpReady: () => "Food Logging Ready",
            chickenBreast: () => "Chicken Breast",
            sugar: () => "Sugar",
            oliveOil: () => "Olive Oil",
            explanation: () => "Your actual meal plan has many foods, but this format lets you log it quickly in your favourite fitness app using 3 basic ingredients that represent your macros.",
        },
        footer: {
            contact: () => "Contact me at:",
        },
        landingPage: {
            navbar: {
                slogen: () => "Your macros. Their food. We do the math.",
                howItWorks: () => "How It Works",
                about: () => "About",
            },
            hero: {
                title: () => "Plan your diet with meals from CityFood and InterFood",
                subtitle: () => "If you want to hit your macros but don’t want to cook, " +
                    "Forktimize creates a daily meal plan using foods from CityFood or InterFood — based on your nutrition goals.",
                orderIfYouLikeIt: () => "If you like the plan, you can order it directly from their website.",
                forkPlan: () => "Fork me a meal plan",
                disclaimer: () => "<strong>Disclaimer:</strong> Forktimize is an independent tool and is not affiliated " +
                    "with endorsed by, or officially connected to CityFood or InterFood. " +
                    "All product names, trademarks, and registered trademarks are property of their respective owners.",
            }
        }

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
            caloriesSmall: () => "kalória",
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
        feedback: {
            ready: () => "Az étrended elkészült.",
            inProgress: () => "Étrend generálása folyamatban... Kérlek, várj!",
            failed: () =>
                `Sajnáljuk, nem találtunk olyan étrendet, ami megfelelne az igényeidnek. 😔 <strong>Próbáld újra más beállításokkal!</strong>`,
            notStarted: () =>
                `Még nincs étrend generálva. Kattints a <strong>„Étrend generálása”</strong> gombra a kezdéshez!`,
        },
        instructions: {
            needHelp: () => "Kell segítség?",
            addGoals: () => `Add meg a <strong>táplálkozási céljaidat</strong> (kalória, fehérje, szénhidrát, zsír).`,
            enterMinMax: () => `Elég csak a <strong>minimum vagy maximum</strong> értéket megadni.`,
            selectDay: () => `<strong>Válaszd ki a napot</strong>, amelyre rendelni szeretnél.`,
            appGenerate: () => `Az alkalmazás egy <strong>étrendet generál</strong>, ami megfelel az igényeidnek.`,
            addDislikedFood: () => `Ha van olyan étel, amit nem szeretsz, <strong>add hozzá a „Nem szeretem” mezőhöz</strong>, hogy kizárjuk őket.`,
            minimizePrice: () => `A <strong>generátor előnyben részesíti az olcsóbb kombinációkat</strong>, miközben figyelembe veszi a megadott célokat.`,
            lessConstraintBetter: () => `Minél <strong>több megkötést adsz meg, annál nehezebb</strong> egy olcsó étrendet találni.`
        },
        summary: {
            title: () => "Az étrended összefoglalása",
            macroRatio: () => "Makrotápanyag arány",
        },
        foodLog: {
            title: () => "Makró Ekvivalens",
            subtitle: () => "Naplózható formátum",
            mfpReady: () => "Ételnapló kompatibilis",
            chickenBreast: () => "Csirkemell",
            sugar: () => "Cukor",
            oliveOil: () => "Olívaolaj",
            explanation: () => "Az étrended sok különböző ételből áll, de ez a formátum lehetővé teszi, hogy gyorsan naplózd kedvenc fitness alkalmazásodba 3 alap összetevő segítségével, amelyek a makróidat képviselik.",
        },
        footer: {
            contact: () => "Kapcsolatfelvétel:",
        },
        landingPage: {
            navbar: {
                slogen: () => "A te makród. Az ő kajájuk. Mi számolunk.",
                howItWorks: () => "Hogyan működik?",
                about: () => "Rólunk",
            },
            hero: {
                title: () => "Étrend tervezés CityFood és InterFood ételeiből",
                subtitle: () => "Ha szeretnéd elérni a makró céljaidat, de nincs kedved főzni, " +
                    "a Forktimize napi étrendet készít neked a <strong>CityFood vagy InterFood</strong> kínálatából – a táplálkozási céljaid alapján.",
                orderIfYouLikeIt: () => "Ha tetszik a terv, az ételt közvetlenül megrendelheted a szolgáltató oldalán.",
                forkPlan: () => "Tervezd meg az étrendem!",
                disclaimer: () => "<strong>Figyelem:</strong> A Forktimize egy független eszköz, " +
                    "nincs kapcsolatban, sem hivatalos együttműködésben a CityFood vagy InterFood cégekkel. " +
                    "Minden terméknév, védjegy és bejegyzett márkanév a tulajdonosát illeti.",
            }
        }

    },
};
