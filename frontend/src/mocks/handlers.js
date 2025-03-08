import {http, HttpResponse} from 'msw'

export const handlers = [

    http.get('*/dates', () => {
        return HttpResponse.json(["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04", "2025-01-05"]);
    }),

    http.post('*/menu', () => {
        // return HttpResponse.json({
        //     foods: []});
        // return HttpResponse(null, {status: 500});
        return HttpResponse.json({
            foods: [
                {
                    food_id: 3125,
                    name: "Saláta",
                    kcal: 850,
                    protein: 65,
                    carbs: 100,
                    fat: 30,
                    price: 1890,
                    date: "2025-01-01"
                },
                {
                    food_id: 3126,
                    name: "Csirkepörkölt krumplival",
                    kcal: 850,
                    protein: 65,
                    carbs: 100,
                    fat: 30,
                    price: 1890,
                    date: "2025-01-01"
                },
                {
                    food_id: 3127,
                    name: "Quinoa Salad",
                    kcal: 380,
                    protein: 10,
                    carbs: 15,
                    fat: 32,
                    price: 1890,
                    date: "2025-01-01"
                },
                {
                    food_id: 3128,
                    name: "Brünni sertésborda (mustárban pácolt) rántva, rizi-bizi",
                    kcal: 650,
                    protein: 45,
                    carbs: 10,
                    fat: 35,
                    price: 2890,
                    date: "2025-01-01"
                },
                {
                    food_id: 3129,
                    name: "Rántott fasza sajt",
                    kcal: 850,
                    protein: 65,
                    carbs: 100,
                    fat: 30,
                    price: 1890,
                    date: "2025-01-01"
                }]
        });
    }),


];
