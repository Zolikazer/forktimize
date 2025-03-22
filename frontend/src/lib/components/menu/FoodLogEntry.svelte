<script>
    import {menuStore} from "$lib/stores/menuStore.js";
    import MacroEquivalent from "$lib/components/menu/equivalent/MacroEquivalent.svelte";
</script>

<div class="box has-text-centered mt-4">
    <h2 class="title border-bottom is-4 has-text-centered has-text-weight-bold pb-3 mb-4">Macro Equivalents (Trackable
        Format)</h2>
    <div class="macro-summary">
        <MacroEquivalent
                emoji="🐔"
                label="Chicken Breast"
                value={$menuStore.foodLogEntry.chicken}
                unit="g"
        />

        <MacroEquivalent
                emoji="🍯"
                label="Sugar"
                value={$menuStore.foodLogEntry.sugar}
                unit="g"
        />

        <MacroEquivalent
                emoji="🫒"
                label="Olive Oil"
                value={$menuStore.foodLogEntry.oil}
                unit="g"
        />

    </div>
    <div class="notification is-info has-text-centered mt-5">
        <strong>
            <span class="icon has-tooltip-multiline">
                <i class="fas fa-info-circle"></i>
            </span>Your actual menu has many foods, but this format lets you log it quickly in your favourite fitness app using 3 basic ingredients that represent your macros.</strong>
    </div>
</div>

<style>
    .macro-summary {
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        margin-top: 1.5rem;
    }

    .macro-box {
        flex: 1;
        background: #f0f0f0;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    }

    .macro-box h3 {
        margin-bottom: 0.25rem;
        font-weight: bold;
        font-size: 1.1rem;
    }

    .macro-emoji {
        font-size: 1.8rem;
        display: block;
        margin-bottom: 0.3rem;
    }

    @media (max-width: 600px) {
        .macro-summary {
            flex-direction: column;
        }
    }
</style>
