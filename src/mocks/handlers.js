import { http, HttpResponse } from 'msw'

export const handlers = [

    http.get('https://example.com/dates', () => {
        // ...and respond to them using this JSON response.
        return HttpResponse.json(["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04", "2025-01-05"]);
    }),


];
