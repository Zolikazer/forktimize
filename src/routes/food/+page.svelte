<script>
    import Input from "./Input.svelte";
    import Result from "./MenuResult.svelte";

    let menu = [];

    function generateMenu() {
        menu = [
            {name: "Grilled Chicken", calories: 300, protein: 40, carbs: 5, fats: 7, price: 3.50},
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
                <Result {menu}/>
            </div>
        </div>
    </div>
</section>



