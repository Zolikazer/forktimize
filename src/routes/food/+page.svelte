<script>
    import Input from "./Input.svelte";
    import Hero from "./Hero.svelte";
    import Result from "./Result.svelte";

    let menu = [];

    function generateMenu() {
        menu = [
            { name: "Grilled Chicken", calories: 300, protein: 40, carbs: 5, fats: 7, price: 3.50 },
            { name: "Quinoa Salad", calories: 250, protein: 8, carbs: 45, fats: 4, price: 2.00 }
        ];
    }
</script>

<style>
    /* Main container for two-column layout */
    .main-container {
        display: flex;
        justify-content: center;
        gap: 2rem;
        max-width: 1200px;
        margin: 2rem auto;
    }

    /* Left side (Input Section) */
    .left-column {
        flex: 1;
        min-width: 45%;
    }

    /* Right side (How to Use) */
    .right-column {
        flex: 1;
        min-width: 45%;
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.4);
    }

    .how-to-title {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #00d1b2;
        text-align: center;
    }

    .how-to-step {
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        margin-bottom: 1rem;
    }

    .how-to-step-icon {
        font-size: 1.5rem;
        color: #00d1b2;
    }
</style>

<Hero />

<div class="main-container">
    <!-- Left Side: Input Section -->
    <div class="left-column">
        <Input {generateMenu}/>
    </div>

    <!-- Right Side: How to Use Section -->
    <div class="right-column">
        <h2 class="how-to-title">How to Use 🍽️</h2>

        <div class="how-to-step">
            <span class="how-to-step-icon">🎯</span>
            <p><strong>Step 1:</strong> Set your nutritional goals (calories, protein, carbs, fats).</p>
        </div>

        <div class="how-to-step">
            <span class="how-to-step-icon">🍏</span>
            <p><strong>Step 2:</strong> Add any dietary restrictions (allergies, hated foods, etc.).</p>
        </div>

        <div class="how-to-step">
            <span class="how-to-step-icon">⚡</span>
            <p><strong>Step 3:</strong> Click "Generate My Menu" to get a meal plan!</p>
        </div>

        <div class="how-to-step">
            <span class="how-to-step-icon">📊</span>
            <p><strong>Step 4:</strong> View your customized meal plan with total nutrients & cost.</p>
        </div>

        <div class="how-to-step">
            <span class="how-to-step-icon">🔄</span>
            <p><strong>Step 5:</strong> Adjust settings and regenerate if needed!</p>
        </div>
    </div>
</div>
<Result {menu}/>
