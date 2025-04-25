<script>
    export let title;
    export let subTitle = ""

</script>

<header class="card-header p-1 has-background-primary has-text-white">
    <div class="card-header-title is-flex is-justify-content-space-between
                is-align-items-center is-flex-wrap-wrap">
        <div>
            <p class="title is-size-5 has-text-black mb-1 has-text-black-100">{title}</p>
            <p class="subtitle is-size-6 has-text-black shadow-text has-text-black-20">
                {@html subTitle}
            </p>
        </div>

        <div class="is-flex is-align-items-center is-flex-wrap-wrap gap-2 mt-2 mt-0-tablet">
            <slot name="tags"></slot>
        </div>
    </div>
</header>

<style>
    .shadow-text {
        text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.15);
    }

</style>
