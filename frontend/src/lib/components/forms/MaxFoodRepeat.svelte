<script>
    let foodCanRepeat = true;
    export let maxFoodRepeat = null;

    $: maxFoodRepeat = foodCanRepeat ? null : 1;
</script>

<div class="field has-text-centered">
    <p class="label mb-2">Can a Food Repeat?</p>
    <div class="is-flex is-justify-content-center is-align-content-center">
        <label class="checkbox is-large custom-green-checkbox">
            <input
                    type="checkbox"
                    bind:checked={foodCanRepeat}
                    class="custom-checkbox"
            >
        </label>
    </div>
</div>

<style>
    .custom-green-checkbox input[type="checkbox"] {
        width: 2rem;
        height: 2rem;
        margin-right: 0.5rem;
        cursor: pointer;

        appearance: none;
        border: 2px solid #b5b5b5;
        border-radius: 4px;
        outline: none;
        transition: all 0.3s;
    }

    .custom-green-checkbox input[type="checkbox"]:not(:checked) {
        background-color: white;
    }

    .custom-green-checkbox input[type="checkbox"]:checked {
        background-color: #48c774;
        border-color: #48c774;

        position: relative;
    }

    .custom-green-checkbox input[type="checkbox"]:checked::after {
        content: '✓';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: white;
        font-weight: bold;
        font-size: 1.5rem;
    }

    .custom-green-checkbox input[type="checkbox"]:hover {
        opacity: 0.8;
    }

    .custom-green-checkbox input[type="checkbox"]:focus {
        box-shadow: 0 0 0 0.125em rgba(72, 199, 116, 0.25);
    }
</style>
