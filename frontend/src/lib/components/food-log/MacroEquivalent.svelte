<script>
    export let icon;
    export let label;
    export let value;
    export let unit;
</script>

<div class="macro-box has-text-centered p-4 has-radius-large">
    <img alt={label}
         src={icon}
         width="50"
         height="50"
         class="has-radius-large"
    />
    <h3 class="has-text-weight-bold is-size-6 mb-1">{label}</h3>
    <p class="has-text-weight-bold">{value} {unit}</p>
</div>

<style>
    .macro-box {
        background: #f0f0f0;

        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .macro-box:hover {
        transform: translateY(-4px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }

</style>
