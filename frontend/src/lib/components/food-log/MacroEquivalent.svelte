<script>
    export let icon = "❓";
    export let label = "Nutrient";
    export let value = 0;
    export let unit = "g";
</script>

<div class="macro-box">
<!--    <span class="macro-emoji">{emoji}</span>-->
    <img alt={label}
         src={icon}
         width="50"
         height="50"
         class="has-radius-large"
    />
    <h3>{label}</h3>
    <p class="has-text-weight-bold">{value} {unit}</p>
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

    .macro-box h3 {
        margin-bottom: 0.25rem;
        font-weight: bold;
        font-size: 1.1rem;
    }

    .macro-emoji {
        font-size: 1.8rem;
        display: block;
        margin-bottom: 0.3rem;
    }

</style>
