<script>
    // Props
    export let emoji = "❓";
    export let label = "Nutrient";
    export let value = 0;
    export let unit = "g"; // Default unit is grams
</script>

<div class="macro-box">
    <span class="macro-emoji">{emoji}</span>
    <h3>{label}</h3>
    <p>{value} {unit}</p>
</div>

<style>
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
