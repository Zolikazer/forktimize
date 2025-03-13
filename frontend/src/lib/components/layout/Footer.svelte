<script>
    const footerText = "© 2025 Menu Maker Pro App created by Zoltán Spagina and ChatGPT 👨‍💻👊🤖";
</script>

<footer class="footer footer-custom mt-5">
    <div class="container">
        <p class="has-text-centered is-size-6 has-text-weight-bold footer-text">{footerText}</p>
    </div>
</footer>

<style>
    .footer-custom {
        background: linear-gradient(135deg, #00d1b2, #009e8e);
        /*url("https://www.transparenttextures.com/patterns/food.png");*/
        background-blend-mode: overlay;
        padding: 1rem 1rem;
        text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.2);
        animation: floatUpDown 3s ease-in-out infinite alternate;
    }

    .footer-text {
        display: inline-block;
        transition: transform 0.3s ease-in-out;
    }

    .footer-text:hover {
        transform: scale(1.05);
    }
</style>
