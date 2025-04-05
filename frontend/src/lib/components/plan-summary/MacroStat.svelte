<script>
    export let icon;
    export let label;
    export let value;
    export let subValue = null;
</script>

<div class="is-flex is-flex-direction-column is-align-items-center box macro-box">
<!--  <span class="icon is-medium mb-1 macro-emoji">-->
<!--    {icon}-->
<!--  </span>-->

    <img alt={label}
         src={icon}
         width="100"
         height="100"
         class="has-radius-large"
    />

    <p class="is-size-8 has-text-grey has-text-weight-bold mb-0">{label}</p>

    <p class="is-size-5 has-text-weight-bold mb-0">{value}</p>

    {#if subValue !== null}
        <p class="is-size-7 has-text-grey mb-0">{subValue}</p>
    {/if}
</div>

<style>
    .macro-box {
        flex: 1;
        background: #f0f0f0;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .macro-box:hover {
        transform: translateY(-4px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }

</style>
