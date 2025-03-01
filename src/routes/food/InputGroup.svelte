<script>
    export let label;
    export let minValue;
    export let maxValue;
    export let unit = "";
</script>

<div class="input-group">
    <p class="group-label">{label}</p>
    <div class="columns is-multiline">
        <div class="column is-half form-group">
            <label class="label">Min {label} ({unit})</label>
            <input type="number" bind:value={minValue} class="input">
        </div>
        <div class="column is-half form-group">
            <label class="label">Max {label} ({unit})</label>
            <input type="number" bind:value={maxValue} class="input">
        </div>
    </div>
</div>

<style>
    .input-group {
        background: #f9f9f9;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
    }

    .group-label {
        font-size: 1.4rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
</style>
