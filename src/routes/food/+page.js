// src/routes/dates/+page.server.js

export async function load() {
    console.log("BASZODJMEG")
    const res = await fetch("https://example.com/dates");
    // const res = await fetch("https://api.genderize.io/?name=luc");
    if (!res.ok) {
        console.log("Failed to fetch dates");
    } else {
        console.log("succes")
        // const foo = await res.json();
        return  {dates: await res.json()};

        // const dates = await res.json();
        // return { dates };
    }
    return {dates: []};
}
