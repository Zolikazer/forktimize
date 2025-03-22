<script>
    export let icon = "❓";
    export let label = "Label";
    export let value = 0;
    // Optional secondary line (like percentage)
    export let subValue = null;
    export let colorClass = "danger";
</script>

<div class="is-flex is-flex-direction-column is-align-items-center box macro-box">
  <span class="icon is-medium mb-1 has-text-{colorClass} macro-emoji">
    {icon}
  </span>

    <p class="is-size-8 has-text-grey has-text-weight-bold mb-0">{label}</p>

    <p class="is-size-5 has-text-weight-bold mb-0">{value}</p>

    {#if subValue !== null}
        <p class="is-size-7 has-text-grey mb-0">{subValue}</p>
    {/if}
</div>

<style>
    .macro-stat-box {
        border-radius: 4px;
        padding: 0.75rem;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        background-color: #f8f8f8;

    }


    .macro-box {
        flex: 1;
        background: #f0f0f0;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease; /* Smooth animation */
    }

    .macro-box:hover {
        transform: translateY(-4px); /* Slight lift */
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); /* Deeper shadow */
    }


    .macro-emoji {
        font-size: 1.5rem;
        display: block;
        margin-bottom: 0.3rem;
    }

</style>
