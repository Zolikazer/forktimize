<script>
    export let label;
    export let minValue;
    export let maxValue;
    export let unit = "";
</script>

<div class="input-group">
    <p class="group-label">{label} ({unit})</p>
    <div class="input-row">
        <div class="input-container">
            <label class="min-max-label">Min</label>
            <input type="number" bind:value={minValue} class="input small-input" placeholder="Min">
        </div>
        <div class="input-container">
            <label class="min-max-label">Max</label>
            <input type="number" bind:value={maxValue} class="input small-input" placeholder="Max">
        </div>
    </div>
</div>

<style>
    .input-group {
        background: #f9f9f9;
        padding: 0.8rem;
        border-radius: 8px;
        box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.1);
        text-align: center;
        font-size: 0.9rem;
        width: 180px; /* Adjusted width to fit inline */
    }

    .group-label {
        font-weight: bold;
        margin-bottom: 0.5rem;
        font-size: 0.85rem;
    }

    .input-row {
        display: flex;
        gap: 0.5rem;
        justify-content: center;
    }

    .input-container {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .min-max-label {
        font-size: 0.75rem;
        font-weight: bold;
        margin-bottom: 2px;
        color: #555;
    }

    .small-input {
        width: 60px;
        padding: 0.3rem;
        font-size: 0.85rem;
        border: 1px solid #ddd;
        border-radius: 5px;
        text-align: center;
    }
</style>
