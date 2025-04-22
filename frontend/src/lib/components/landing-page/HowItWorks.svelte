<script>
    import {t} from "$lib/stores/localeStore.js";
</script>

<section class="section" id="how">
    <div class="container">
        <h2 class="title is-4 has-text-centered mb-4">{$t.landingPage.howItWorks.howItWorks()}</h2>

        <div class="columns">
            <div class="column">
                <div class="box has-text-centered py-4">
                    <i class="fas fa-store has-text-primary mb-2"></i>
                    <h3>{@html $t.landingPage.howItWorks.chooseVendor()}
                    </h3>
                </div>
            </div>
            <div class="column">
                <div class="box has-text-centered py-4">
                    <i class="fas fa-calendar-alt has-text-warning mb-2"></i>
                    <h3>{@html $t.landingPage.howItWorks.setDate()}</h3>
                </div>
            </div>
            <div class="column">
                <div class="box has-text-centered py-4">
                    <i class="fas fa-bullseye has-text-link mb-2"></i>
                    <h3>{@html $t.landingPage.howItWorks.setMacros()}</h3>
                </div>
            </div>

            <div class="column">
                <div class="box has-text-centered py-4">
                    <i class="fas fa-utensils has-text-danger mb-2"></i>
                    <h3>{@html $t.landingPage.howItWorks.getPlan()}</h3>
                </div>
            </div>
            <div class="column">
                <div class="box has-text-centered py-4">
                    <i class="fas fa-receipt has-text-info mb-2"></i>
                    <h3>{@html $t.landingPage.howItWorks.orderFood()}</h3>
                </div>
            </div>
        </div>
    </div>
</section>

<style>
    .columns {
        align-items: stretch;
    }

    .box {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;

        padding: 1.5rem;
        min-height: 150px;
        transition: transform 0.2s ease;
    }

    .box:hover {
        transform: translateY(-4px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }

</style>
