<script>
    import {t} from '$lib/stores/localeStore.js';

    let showModal = false;
</script>

<section class="hero is-small has-background-light">
    <div class="hero-body">
        <div class="container">
            <div class="columns is-vcentered">
                <div class="column is-8">
                    <h1 class="title is-3">
                        Forktimize: {$t.landingPage.hero.title()}
                    </h1>
                    <!--                    <h2 class="subtitle">-->
                    <!--                        Your macros. Their food. We do the math.-->
                    <!--                    </h2>-->
                    <p class="subtitle is-6">
                        {@html $t.landingPage.hero.subtitle()}
                    </p>
                    <p>{$t.landingPage.hero.orderIfYouLikeIt()}</p>
                    <a href="/meal-plan-generator" class="button is-primary is-rounded mt-2 shadow-text">
                        {$t.landingPage.hero.forkPlan()}
                    </a>
                    <p class="subtitle is-7 mt-2">
                        {@html $t.landingPage.hero.disclaimer()}
                    </p>
                </div>
                <div class="column is-4">
                    <figure class="image is-3by2">
                        <button on:click={() => showModal = true} style="cursor: zoom-in;">
                            <img src="forktimize-preview.png"
                                 alt="Forktimize étrend tervező előnézet – CityFood és InterFood ajánlatok"
                                 class="has-radius-small"/>
                        </button>
                    </figure>
                </div>

                {#if showModal}
                    <div class="modal is-active">
                        <div class="modal-background"></div>
                        <div class="modal-content" style="height: 95vh; width: 100vh">
                            <figure class="image">
                                <img
                                        src="forktimize-preview.png"
                                        alt="Forktimize étrend tervező előnézet – CityFood és InterFood ajánlatok"
                                        class="has-radius-small"
                                        style="height: 95vh; width: 100vh"
                                />
                            </figure>
                        </div>
                        <button class="modal-close is-large"
                                aria-label="close"
                                on:click={() => showModal = false}>
                        </button>
                    </div>
                {/if}
            </div>
        </div>
    </div>
</section>
