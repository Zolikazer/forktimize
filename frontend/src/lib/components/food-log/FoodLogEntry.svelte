<script>
    import {mealPlanStore} from "$lib/stores/mealPlanStore.js";
    import SectionHeader from "$lib/components/common/SectionHeader.svelte";
    import MacroEquivalent from "$lib/components/food-log/MacroEquivalent.svelte";
</script>

<div class="card mt-4">
    <SectionHeader title="Macro Equivalents" subTitle="Trackable Format">
        <span class="tag is-success is-light bigger-tag" slot="tags">📲 MyFitnessPal Ready</span>

    </SectionHeader>
    <div class="columns is-mobile is-4 mt-4 px-5">
        <div class="column">
            <MacroEquivalent
                    icon="chicken-breast.png"
                    label="Chicken Breast"
                    value={$mealPlanStore.foodLogEntry.chicken}
                    unit="g"
            />
        </div>

        <div class="column">
            <MacroEquivalent
                    icon="honey.png"
                    label="Sugar"
                    value={$mealPlanStore.foodLogEntry.sugar}
                    unit="g"
            />
        </div>

        <div class="column">
            <MacroEquivalent
                    icon="olive.png"
                    label="Olive Oil"
                    value={$mealPlanStore.foodLogEntry.oil}
                    unit="g"
            />
        </div>

    </div>
    <div class="notification is-info has-text-centered mt-5">
        <strong>
            <span class="icon has-tooltip-multiline">
                <i class="fas fa-info-circle"></i>
            </span>Your actual meal plan has many foods, but this format lets you log it quickly in your favourite
            fitness app using 3 basic ingredients that represent your macros.</strong>
    </div>
</div>
