<script>
    import Food from "$lib/components/app/Food.svelte";

    let aFood = {
        name: "Brünni sertésborda (mustárban pácolt) rántva, rizi-bizi",
        calories: 300,
        protein: 400,
        carbs: 100,
        fats: 78,
        price: 2565
    };

</script>

<div class="box">
    <h2 class="title border-bottom is-4 has-text-centered has-text-weight-bold pb-3 mb-4">Your Menu On Wednesday</h2>

    <div class="is-flex is-flex-wrap-wrap is-justify-content-center">
            <Food food={aFood}/>
            <Food food={aFood}/>
            <Food food={aFood}/>
            <Food food={aFood}/>
            <Food food={aFood}/>
        </div>
</div>
