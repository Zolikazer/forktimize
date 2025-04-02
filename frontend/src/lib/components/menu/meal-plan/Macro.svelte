<script>
    export let macroName;
    export let macroValue;
    export let macroRatio;
    export let ratioColorClass;

</script>

<div class="mb-2">
    <div class="is-flex is-align-items-center mb-1">
        <span class="mr-1">💪</span>
        <span class="is-flex-grow-1 is-size-7">{macroName}</span>
        <span class="has-text-weight-bold is-size-7">{macroValue}g</span>
    </div>
    <div class="progress-bar">
        <div class="progress-fill {ratioColorClass}" style="width: {macroRatio}%"></div>
    </div>
</div>

<style>
    .progress-bar {
        height: 6px;
        background-color: #f0f0f0;
        border-radius: 3px;
        overflow: hidden;
    }

    .progress-fill {
        height: 100%;
        border-radius: 3px;
    }
</style>
