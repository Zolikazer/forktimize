<script>
    const providers = ["CityFood", "Interfood"];
    let selected = "CityFood";
</script>

<div class="field tag is-light is-success bigger-tag is-flex is-justify-content-space-between is-align-items-center">
    <span>🧑‍🍳 Kitchen:</span>
    <div class="control is-light ml-1">
        <div class="select is-primary is-small styled-select">
            <select bind:value={selected}>
                {#each providers as provider}
                    <option value={provider}>{provider}</option>
                {/each}
            </select>
        </div>
    </div>
</div>

<style>

    .styled-select select {
        background-color: #f5f5f5;
        border: none;
        font-weight: bold;
        color: #363636;
        cursor: pointer;

        font-size: 1.1rem;
        line-height: 1;
        padding-top: 0.2rem;
        padding-bottom: 0.2rem;
        height: 1.8em;

    }

    .styled-select select:hover {
        background-color: #eeeeee;
    }

    .styled-select select:focus {
        box-shadow: 0 0 0 0.125em rgba(0, 209, 178, 0.25);
    }


</style>
