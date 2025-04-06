<script>
    import LanguageSelector from "$lib/components/layout/LanguageSelector.svelte";
</script>

<nav class="navbar is-primary " aria-label="main navigation">
    <div class="container">
        <div class="navbar-brand">
            <a class="navbar-item shadow-text is-size-5 has" href="/">
                <i class="fas fa-utensils mr-2"></i>
                <span><strong>Forktimize</strong> - Your macros. Their food. We do the math.</span>
            </a>
        </div>
        <div class="navbar-end">
            <a class="navbar-item shadow-text" href="#how">How It Works</a>
            <a class="navbar-item shadow-text" href="#about">About</a>
            <a class="navbar-item shadow-text" href="https://github.com/zolikazer/forktimize" target="_blank"
               rel="noopener noreferrer">
                <i class="fab fa-github mr-1"></i> GitHub
            </a>
            <div class="navbar-item"><LanguageSelector/></div>
        </div>
    </div>
</nav>
