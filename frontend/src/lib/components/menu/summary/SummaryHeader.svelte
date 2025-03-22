<script>
    // We'll accept these props from the parent
    // Adjust as needed for your actual data structures
    export let title = "Your Meal Plan";
    export let planDate = new Date();
    export let totalCalories = 0;
    export let totalPrice = 0;

    // Optionally pass in custom formatters
    export let formatDate = (date) =>
        date.toLocaleDateString("en-US", {
            weekday: "long",
            month: "long",
            day: "numeric",
            year: "numeric"
        });

    export let formatPrice = (price) =>
        new Intl.NumberFormat("en-US", {
            style: "currency",
            currency: "USD"
        }).format(price);
</script>

<header class="card-header p-1 has-background-primary has-text-white">
    <div class="card-header-title is-flex is-justify-content-space-between
              is-align-items-center is-flex-wrap-wrap">
        <div>
            <p class="title is-size-4 has-text-black mb-1">{title}</p>
            <p class="subtitle is-size-6 has-text-black">
                For {formatDate(planDate)}
            </p>
        </div>

        <!-- Right Side: Quick Stats (Calories, Price) -->
        <div class="is-flex is-align-items-center is-flex-wrap-wrap gap-2 mt-2 mt-0-tablet">
            <div class="tags">
              <span class="tag is-info is-light bigger-tag">
                🔥 {totalCalories.toLocaleString("fr-FR")} calories
              </span>
                <span class="tag is-success is-light bigger-tag">
                💸 {totalPrice.toLocaleString("fr-FR")} Ft
              </span>
            </div>
        </div>
    </div>
</header>

<style>
    .bigger-tag {
        font-size: 1.2rem; /* pick whatever size you want */
    }
</style>
