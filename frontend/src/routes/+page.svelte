<script>
    let isActive = false;

    function toggleNavbar() {
        isActive = !isActive;
    }
</script>

<svelte:head>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</svelte:head>

<!-- Simple navbar -->
<nav class="navbar is-light" aria-label="main navigation">
    <div class="container">
        <div class="navbar-brand">
            <a class="navbar-item" href="/">
        <span class="icon mr-2">
          <i class="fas fa-utensils"></i>
        </span>
                <span class="has-text-weight-bold">Forktimize</span>
            </a>

            <a role="button" class="navbar-burger" class:is-active={isActive} aria-label="menu" aria-expanded="false" on:click={toggleNavbar}>
                <span aria-hidden="true"></span>
                <span aria-hidden="true"></span>
                <span aria-hidden="true"></span>
            </a>
        </div>

        <div class="navbar-menu" class:is-active={isActive}>
            <div class="navbar-end">
                <a class="navbar-item" href="#how-it-works">How It Works</a>
                <a class="navbar-item" href="#about">About</a>
                <a class="navbar-item" href="https://github.com/forktimize">
          <span class="icon">
            <i class="fab fa-github"></i>
          </span>
                    <span>GitHub</span>
                </a>
            </div>
        </div>
    </div>
</nav>

<!-- Simple hero section -->
<section class="hero is-medium has-background-light">
    <div class="hero-body">
        <div class="container">
            <div class="columns is-vcentered">
                <div class="column is-7">
                    <h1 class="title is-2 mb-4">
                        Hey there! We're Forktimize 👋
                    </h1>
                    <p class="subtitle is-5 mb-5">
                        A fun little project that helps you plan meals using real food from local providers.
                        No more generic recipes - we use actual orderable food and some smart algorithms to make meal planning easier.
                    </p>
                    <a href="#generate" class="button is-primary is-rounded is-medium">
                        <span>Fork me a meal plan</span>
                        <span class="icon">
              <i class="fas fa-utensils"></i>
            </span>
                    </a>
                </div>
                <div class="column is-5">
                    <figure class="image">
                        <img src="https://images.unsplash.com/photo-1543352634-99a5d50ae78e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80" alt="Healthy meal options">
                    </figure>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- How it works - simplified -->
<section class="section" id="how-it-works">
    <div class="container">
        <h2 class="title is-3 has-text-centered mb-5">How It Works</h2>

        <div class="columns is-multiline">
            <div class="column is-4">
                <div class="box has-text-centered">
          <span class="icon is-large mb-3">
            <i class="fas fa-store fa-2x has-text-primary"></i>
          </span>
                    <h3 class="title is-5">1. Pick a Food Provider</h3>
                    <p>Choose from local food vendors that deliver in your area.</p>
                </div>
            </div>

            <div class="column is-4">
                <div class="box has-text-centered">
          <span class="icon is-large mb-3">
            <i class="fas fa-calendar-alt fa-2x has-text-warning"></i>
          </span>
                    <h3 class="title is-5">2. Set Your Dates</h3>
                    <p>Tell us when you need your meals - today, tomorrow, or next week.</p>
                </div>
            </div>

            <div class="column is-4">
                <div class="box has-text-centered">
          <span class="icon is-large mb-3">
            <i class="fas fa-utensils fa-2x has-text-danger"></i>
          </span>
                    <h3 class="title is-5">3. Get Your Plan</h3>
                    <p>We'll suggest a balanced meal plan from what's actually available.</p>
                </div>
            </div>
        </div>
    </div>
</section>

<section class="section has-background-white-bis" id="generate">
    <div class="container">
        <div class="box has-text-centered p-5">
            <h2 class="title is-3 mb-3">Want to try it out?</h2>
            <p class="mb-4">Our little algorithm is ready to help you plan some tasty meals!</p>
            <a href="#" class="button is-warning is-medium is-rounded">
                <span>Optimize my food</span>
            </a>
        </div>
    </div>
</section>

<section class="section" id="about">
    <div class="container">
        <div class="columns is-centered">
            <div class="column is-8">
                <div class="content has-text-centered">
                    <h2 class="title is-3 mb-4">About This Project</h2>
                    <p>
                        Forktimize started as a weekend project when we got tired of planning meals that we couldn't actually order.
                        We wanted to create something that uses real food options from local delivery services.
                    </p>
                    <p>
                        This is a passion project and completely open-source. Feel free to contribute or just say hi!
                    </p>
                    <div class="mt-5">
                        <a href="https://github.com/forktimize" class="button is-light">
              <span class="icon">
                <i class="fab fa-github"></i>
              </span>
                            <span>Check us out on GitHub</span>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Simple footer -->
<footer class="footer has-background-light">
    <div class="container">
        <div class="has-text-centered">
            <p>
        <span class="icon mr-2">
          <i class="fas fa-utensils"></i>
        </span>
                <strong>Forktimize</strong> - A little meal planning project
            </p>
            <p class="mt-2">
                <a href="mailto:hello@forktimize.example.com">hello@forktimize.example.com</a>
            </p>
            <p class="mt-4">
                Made with ❤️ and a bit of hunger
            </p>
        </div>
    </div>
</footer>

<style>
    .hero {
        padding-top: 2rem;
    }

    .box {
        transition: transform 0.3s ease;
    }

    .box:hover {
        transform: translateY(-5px);
    }

    @media screen and (max-width: 768px) {
        .hero-body {
            padding: 3rem 1.5rem;
        }
    }
</style>
