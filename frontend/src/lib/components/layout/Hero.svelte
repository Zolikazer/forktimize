<script>
    import {getVendorLabel} from "$lib/utils/foodVendors.js";
    import {mealPlanRequestStore} from "$lib/stores/mealPlanRequestStore.js";

    export let title = "CityFood Meal Planner 🥗🍽️";
    export let subtitle = "Tervezz, Zabálj, Be Fit!";

    $: title = `${getVendorLabel($mealPlanRequestStore.foodVendor)} Meal Planner 🥗🍽️`;
</script>


<section class="hero hero-custom">
    <div class="hero-body has-text-centered hero-content">
        <div class="container">
            <h1 class="title hero-title title-animated">{title}</h1>
            <p class="subtitle hero-subtitle">{subtitle}</p>
            <!--            <button class="button hero-button">Get Started 🚀</button>-->
        </div>
    </div>
</section>

<style>
    .hero-custom {
        background: linear-gradient(135deg, #00d1b2, #009e8e),
        url("/food.png");
        background-blend-mode: overlay; /* Blends the gradient & pattern */;
        padding: 1.5rem 1rem; /* Reduced padding */
        color: white;
        text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.2);
        animation: floatUpDown 3s ease-in-out infinite alternate;
    }
    .hero-body {
        padding: 1.15rem 0; /* Less vertical spacing */
    }

    .hero-title {
        font-size: 2.5rem; /* Keep large text */
        font-weight: bold;
        margin-bottom: 0.5rem; /* Reduce space below title */
    }

    .hero-subtitle {
        font-size: 1.4rem; /* Keep subtitle large */
        margin-bottom: 1rem; /* Reduce space below subtitle */
    }

    /* Fun text bounce effect */
    .title-animated {
        display: inline-block;
        transition: transform 0.3s ease-in-out;
    }

    .title-animated:hover {
        transform: scale(1.1);
    }

    .hero-button {
        background: white;
        color: #00d1b2;
        font-size: 1.1rem;
        font-weight: bold;
        padding: 0.75rem 1.5rem;
        border-radius: 50px;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.2);
    }

    .hero-button:hover {
        background: #f0fdfa;
        transform: scale(1.05);
        box-shadow: 0 5px 10px rgba(0, 0, 0, 0.3);
    }

    .hero-content {
        animation: floatUp 2s ease-in-out infinite alternate;
    }

    @keyframes floatUp {
        from {
            transform: translateY(0);
        }
        to {
            transform: translateY(-5px);
        }
    }
</style>
