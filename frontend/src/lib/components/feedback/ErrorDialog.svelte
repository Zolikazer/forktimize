<script>
    import { errorStore, hideError } from "$lib/stores/errorStore.js";
</script>

{#if $errorStore.show}
    <div class="modal is-active">
        <div class="modal-background"></div>
        <div class="modal-card">
            <header class="modal-card-head">
                <p class="modal-card-title">Error 😱</p>
                <button class="delete" aria-label="close" on:click={hideError}></button>
            </header>
            <section class="modal-card-body">
                <div class="notification is-danger has-text-centered">
                    <p><strong> {$errorStore.message}</strong></p>
                    <p>Please try again! ⚠️</p>
                </div>
            </section>
            <footer class="modal-card-foot">
                <button class="button is-danger is-light" on:click={hideError}>Close</button>
            </footer>
        </div>
    </div>
{/if}
