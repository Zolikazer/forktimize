<script>
    import {mealPlanStore} from "$lib/stores/mealPlanStore.js";
    import SectionHeader from "$lib/components/common/SectionHeader.svelte";
    import MacroEquivalent from "$lib/components/food-log/MacroEquivalent.svelte";
    import {t} from '$lib/stores/localeStore.js';
</script>

<div class="card mt-4">
    <SectionHeader title={$t.foodLog.title()} subTitle={$t.foodLog.subtitle()}>
        <span class="tag is-success is-light bigger-tag" slot="tags">📲 {$t.foodLog.mfpReady()}</span>
    </SectionHeader>
    <div class="columns is-mobile is-4 mt-4 px-5">
        <div class="column">
            <MacroEquivalent
                    icon="chicken-breast.webp"
                    label={$t.foodLog.chickenBreast()}
                    value={$mealPlanStore.foodLogEntry.chicken}
                    unit="g"
            />
        </div>

        <div class="column">
            <MacroEquivalent
                    icon="honey.webp"
                    label={$t.foodLog.sugar()}
                    value={$mealPlanStore.foodLogEntry.sugar}
                    unit="g"
            />
        </div>

        <div class="column">
            <MacroEquivalent
                    icon="olive.webp"
                    label={$t.foodLog.oliveOil()}
                    value={$mealPlanStore.foodLogEntry.oil}
                    unit="g"
            />
        </div>

    </div>
    <div class="notification is-info has-text-centered mt-5">
        <strong>
            <span class="icon has-tooltip-multiline">
                <i class="fas fa-info-circle"></i>
            </span>{$t.foodLog.explanation()}</strong>
    </div>
</div>
