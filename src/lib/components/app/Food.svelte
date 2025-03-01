<script>
    export let food; // Pass food object as a prop
</script>

<div class="card food-card">
    <div class="card-image">
        <figure class="image is-16by9">
            <img
                    src="https://bulma.io/assets/images/placeholders/1280x960.png"
                    alt="Placeholder image"
            />
        </figure>
    </div>
    <div class="card-content">
        <div class="media">
            <div class="media-content">
                <p class="title is-5">{food.name}</p>
                <p class="subtitle is-6">{food.price} Ft</p>
            </div>
        </div>

        <div class="columns is-centered">
            <div class="column">
                <div><strong>🔥 {food.calories}</strong> kcal kalória</div>
            <div><strong>💪 {food.protein}</strong> g fehérje</div>
            </div>
            <div class="column">
                <div><strong>🥖 {food.carbs}</strong> g szénhidrát</div>
                <div><strong>🛢️ {food.fats}</strong> g     zsír</div>
            </div>
        </div>

<!--        <div class="nutrient-grid">-->
<!--            <div><strong>🔥 {food.calories}</strong> kcal</div>-->
<!--            <div><strong>💪 {food.protein}</strong> g fehérje</div>-->
<!--            <div><strong>🥖 {food.carbs}</strong> g szénhidrát</div>-->
<!--            <div><strong>🛢️ {food.fats}</strong> g zsír</div>-->
<!--        </div>-->

        <button class="button is-danger is-light is-fullwidth mt-3" on:click={() => removeFood(food.name)}>
            🤮 Nem szeretem
        </button>
    </div>
</div>

<style>
    .food-card {
        width: 250px;
        border-radius: 12px;
        box-shadow: 0px 3px 8px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease-in-out;
    }

    .food-card:hover {
        transform: scale(1.03);
    }

    .media-content p {
        margin: 0;
    }

</style>
