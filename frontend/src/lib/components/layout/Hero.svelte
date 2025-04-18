<script>
    import {mealPlanRequestStore} from "$lib/stores/mealPlanRequestStore.js";
    import LanguageSelector from "$lib/components/layout/LanguageSelector.svelte";
    import {t} from '$lib/stores/localeStore.js';
    import {vendorListStore} from "$lib/stores/foodVendorStore.js";

    let title;

    $: vendorName =
        $vendorListStore.find(v => v.type === $mealPlanRequestStore.foodVendor)
            ?.name ?? 'Forktimize';

    $: title = `${$t.hero.title({vendor: vendorName})} 🥗🍽️`;

</script>


<section class="hero hero-custom">
    <div class="has-text-centered hero-content py-1">
        <div class="container">
            <LanguageSelector floating={true}/>
            <h1 class="title title-animated is-size-2 has-text-weight-bold mb-2">{title}</h1>
            <p class="subtitle hero-subtitle is-size-4 mb-4">{$t.hero.subtitle()}</p>
        </div>
    </div>
</section>

<style>
    .hero-custom {
        background: linear-gradient(135deg, #00d1b2, #009e8e),
        url("/food.webp");
        background-blend-mode: overlay;
        padding: 1.5rem 1rem;
        color: white;
        text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.2);
        animation: floatUpDown 3s ease-in-out infinite alternate;
    }

    .title-animated {
        display: inline-block;
        transition: transform 0.3s ease-in-out;
    }

    .title-animated:hover {
        transform: scale(1.1);
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
