<script>
    let showModal = false;
</script>

<section class="hero is-small has-background-light">
    <div class="hero-body">
        <div class="container">
            <div class="columns is-vcentered">
                <div class="column is-8">
                    <h1 class="title is-3">
                        Forktimize: Your macros. Their food. We do the math.
                    </h1>
                    <p class="subtitle is-5">
                        If you want to hit your macros but don’t want to cook,
                        Forktimize creates a daily meal plan using foods from <strong>CityFood or InterFood</strong> —
                        based on your nutrition goals.
                    </p>
                    <p>If you like the plan, you can order it directly from their website.</p>
                    <a href="/meal-plan-generator" class="button is-primary is-rounded mt-2 shadow-text">
                        Fork me a meal plan
                    </a>
                    <p class="subtitle is-7 mt-2">
                        <strong>Disclaimer:</strong> Forktimize is an independent tool and is not affiliated with,
                        endorsed by, or officially connected to CityFood or InterFood.
                        All product names, trademarks, and registered trademarks are property of their respective
                        owners.
                    </p>
                </div>
                <div class="column is-4">
                    <figure class="image is-3by2">
                        <button on:click={() => showModal = true} style="cursor: zoom-in;">
                            <img src="forktimize-preview.png" alt="Forktimize preview" class="has-radius-small"/>
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
                                        alt="Preview full"
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
