import {http, HttpResponse} from 'msw'

export const handlers = [

    http.get('*/dates', () => {
        return HttpResponse.json(["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04", "2025-01-05"]);
    }),

    http.post('*/menu', () => {
        return HttpResponse.json({
            foods: [
                {
                    food_id: 3125,
                    name: "Saláta",
                    calories: 850,
                    protein: 65,
                    carb: 100,
                    fat: 30,
                    price: 1890,
                    date: "2025-01-01"
                },
                {
                    food_id: 3126,
                    name: "Csirkepörkölt krumplival",
                    calories: 850,
                    protein: 65,
                    carb: 100,
                    fat: 30,
                    price: 1890,
                    date: "2025-01-01"
                },
                {
                    food_id: 3127,
                    name: "Quinoa Salad",
                    calories: 380,
                    protein: 10,
                    carb: 15,
                    fat: 32,
                    price: 1890,
                    date: "2025-01-01"
                },
                {
                    food_id: 3128,
                    name: "Brünni sertésborda (mustárban pácolt) rántva, rizi-bizi",
                    calories: 650,
                    protein: 45,
                    carb: 10,
                    fat: 35,
                    price: 2890,
                    date: "2025-01-01"
                },
                {
                    food_id: 3129,
                    name: "Rántott fasza sajt",
                    calories: 850,
                    protein: 65,
                    carb: 100,
                    fat: 30,
                    price: 1890,
                    date: "2025-01-01"
                }],
            foodLogEntry: {chicken: 360, sugar: 50, oil: 10}
        });
    }),


];
