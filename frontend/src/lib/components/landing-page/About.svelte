<script>
    import {t} from '$lib/stores/localeStore.js';

</script>
<section class="section" id="about">
    <div class="container">
        <div class="columns is-centered">
            <div class="column is-8">
                <p class="content has-text-centered">
                <h2 class="title is-4 mb-3">{$t.landingPage.about.about()}</h2>

                <p class="mb-4">
                    <strong>🙋 {$t.landingPage.about.whatIsThisTitle()}</strong>
                    <br>
                    {@html $t.landingPage.about.whatIsThisText()}
                </p>

                <p class="mb-4 has-text-weight-bold">
                    {$t.landingPage.about.youTellIt.title()}
                </p>

                <ul class="has-text-left is-inline-block mb-2">
                    <li>• {$t.landingPage.about.youTellIt.goal()}</li>
                    <li>• {$t.landingPage.about.youTellIt.vendor()}</li>
                    <li>• {$t.landingPage.about.youTellIt.date()}</li>
                </ul>

                <p class="mb-4">
                    {$t.landingPage.about.youTellIt.explanation()}
                </p>

                <p class="mb-4">
                    <strong>🧩 {$t.landingPage.about.whyBother.title()}</strong>
                    <br>
                    {$t.landingPage.about.whyBother.lotOptions()}
                </p>

                <p class="mb-4">
                    {$t.landingPage.about.whyBother.itSolves()}
                </p>

                <p class="mb-4">
                    <strong>🧑‍💻 {$t.landingPage.about.whoMade.this()}</strong><br>
                    {$t.landingPage.about.whoMade.me()}
                </p>

                <p class="mb-4">
                    {$t.landingPage.about.whoMade.free()}
                </p>

                <a href="https://github.com/zolikazer/forktimize"
                   class="button is-light is-small mt-3"
                   target="_blank"
                   rel="noopener noreferrer"
                >
                    <i class="fab fa-github mr-1"></i> GitHub
                </a>
            </div>
        </div>
    </div>
</section>
