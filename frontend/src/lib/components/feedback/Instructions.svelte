<script>
    import {t} from '$lib/stores/localeStore.js';

</script>

<div class="box has-background-light p-4 is-rounded shadow">
    <h2 class="title is-5 has-text-centered">📋 {$t.instructions.needHelp()}</h2>
    <ul class="content">
        <li>🎯 {@html $t.instructions.addGoals()}</li>
        <li>⚖️  {@html $t.instructions.enterMinMax()}</li>
        <li>📅 {@html $t.instructions.selectDay()}</li>
        <li>📋 {@html $t.instructions.appGenerate()}</li>
        <li>🚫 {@html $t.instructions.addDislikedFood()}</li>
        <li>💰 {@html $t.instructions.minimizePrice()}</li>
        <li>⚠️ {@html $t.instructions.lessConstraintBetter()}</li>
    </ul>
</div>
