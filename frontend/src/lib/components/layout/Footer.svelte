<script>
    import {t} from '$lib/stores/localeStore.js';

    const emailUser = "spagina.zoltan";
    const emailDomain = "gmail.com";
    const email = `${emailUser}@${emailDomain}`;
</script>

<footer class="footer footer-custom mt-5">
    <div class="container">
        <div class="level">
            <div class="level-left">
                <div class="level-item">
                    <p class="is-size-6 has-text-weight-bold footer-text">
                        © 2025 Forktimize App Coded by Zoltán Spagina
                    </p>
                </div>
            </div>
            <div class="level-right">
                <div class="level-item">
                    <p class="is-size-6 footer-text has-text-weight-bold">
                        {$t.footer.contact()} <a href={`mailto:${email}`} class="has-text-weight-bold has-text-link no-shadow">{email}</a>
                    </p>
                </div>
            </div>
        </div>
    </div>
</footer>

<style>
    .footer-custom {
        background: linear-gradient(135deg, #00d1b2, #009e8e);
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

    .no-shadow {
        text-shadow: none !important;
    }
</style>
