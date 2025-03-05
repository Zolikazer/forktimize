<script>
    import Input from "$lib/components/app/Input.svelte";
    import MenuResult from "$lib/components/app/MenuResult.svelte";
    import Food from "$lib/components/app/Food.svelte";
    import Help from "$lib/components/app/Help.svelte";
    import Menu from "$lib/components/app/Menu.svelte";

    let menu = [];

    let aFood = {
        name: "Brünni sertésborda (mustárban pácolt) rántva, rizi-bizi",
        calories: 300,
        protein: 400,
        carbs: 100,
        fats: 78,
        price: 2565
    };

    function generateMenu() {
        menu = [
            aFood,
            {name: "Quinoa Salad", calories: 250, protein: 8, carbs: 45, fats: 4, price: 2.00}
        ];
    }
</script>

<style>
    /* Main container for two-column layout */
    .main-container {
        display: flex;
        /*justify-content: center;*/
        /*gap: 2rem;*/
        /*max-width: 1200px;*/
        margin: 2rem auto;
    }

</style>


<section class="main-container">
    <div class="container is-fluid">
        <div class="columns is-centered">
            <div class="column">
                <Input {generateMenu}/>
            </div>
            <div class="column">
                <Help/>
            </div>
        </div>

        <div class="columns is-centered">
            <div class="column">
                <Menu/>
            </div>
            <div class="column">
            </div>
        </div>
    </div>
</section>



