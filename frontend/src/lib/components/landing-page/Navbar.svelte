<script>
    let isActive = false;

    function toggleNavbar() {
        isActive = !isActive;
    }
</script>


<nav class="navbar is-primary " aria-label="main navigation">
    <div class="container">
        <div class="navbar-brand">
            <a class="navbar-item shadow-text is-size-5 has" href="/">
                <i class="fas fa-utensils mr-2"></i>
                <span>Forktimize</span>
            </a>

            <a role="button" class="navbar-burger" class:is-active={isActive} aria-label="menu" aria-expanded="false"
               on:click={toggleNavbar}>
                <span aria-hidden="true"></span>
                <span aria-hidden="true"></span>
                <span aria-hidden="true"></span>
            </a>
        </div>

        <div class="navbar-menu" class:is-active={isActive}>
            <div class="navbar-end">
                <a class="navbar-item shadow-text" href="#how">How It Works</a>
                <a class="navbar-item shadow-text" href="#about">About</a>
                <a class="navbar-item shadow-text" href="https://github.com/zolikazer/forktimize" target="_blank"
                   rel="noopener noreferrer">
                    <i class="fab fa-github mr-1"></i> GitHub
                </a>
            </div>
        </div>
    </div>
</nav>
