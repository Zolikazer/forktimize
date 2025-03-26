<script>
    import {menuStore} from "$lib/stores/menuStore.js";
    import MacroEquivalent from "$lib/components/menu/equivalent/MacroEquivalent.svelte";
    import SectionHeader from "$lib/components/common/SectionHeader.svelte";
</script>

<div class="card mt-4">
    <SectionHeader title="Macro Equivalents" subTitle="Trackable Format">
        <span class="tag is-success is-light bigger-tag" slot="tags">📲 MyFitnessPal Ready</span>

    </SectionHeader>
    <div class="macro-summary p-4">
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

    .macro-box h3 {
        margin-bottom: 0.25rem;
        font-weight: bold;
        font-size: 1.1rem;
    }


    @media (max-width: 600px) {
        .macro-summary {
            flex-direction: column;
        }
    }
</style>
