<script>
    import Input from "./Input.svelte";
    import Hero from "./Hero.svelte";
    import Result from "./Result.svelte";

    let menu = [];

    function generateMenu() {
        menu = [
            { name: "Grilled Chicken", calories: 300, protein: 40, carbs: 5, fats: 7, price: 3.50 },
            { name: "Quinoa Salad", calories: 250, protein: 8, carbs: 45, fats: 4, price: 2.00 }
        ];
    }
</script>

<Hero />
<Input {generateMenu}/>
<Result {menu} />
