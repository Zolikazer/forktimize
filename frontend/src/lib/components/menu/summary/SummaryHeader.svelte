<script>
    export let title = "Your Meal Plan";
    export let planDate = new Date();
    export let totalCalories = 0;
    export let totalPrice = 0;

    export let formatDate = (date) =>
        date.toLocaleDateString("hu-HU", {
            weekday: "long",
            month: "long",
            day: "numeric",
            year: "numeric"
        });

</script>

<header class="card-header p-1 has-background-primary has-text-white">
    <div class="card-header-title is-flex is-justify-content-space-between
              is-align-items-center is-flex-wrap-wrap">
        <div>
            <p class="title is-size-5 has-text-black mb-1 has-text-black-100">{title}</p>
            <p class="subtitle is-size-6 has-text-black shadow-text has-text-black-20">
                📅 {formatDate(new Date(planDate))}
            </p>
        </div>

        <div class="is-flex is-align-items-center is-flex-wrap-wrap gap-2 mt-2 mt-0-tablet">
            <div class="tags">
                <span class="tag is-success is-light bigger-tag">
                💸 {totalPrice.toLocaleString("fr-FR")} Ft
              </span>
                <span class="tag is-info is-light bigger-tag">
                🔥 {totalCalories.toLocaleString("fr-FR")} calories
              </span>
            </div>
        </div>
    </div>
</header>

<style>
    .bigger-tag {
        font-size: 1.2rem;
    }

    .shadow-text {
        text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.15);
    }

</style>
