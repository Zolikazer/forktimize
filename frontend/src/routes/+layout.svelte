<script>
    import '../app.css';
    import Hero from "$lib/components/layout/Hero.svelte";
    import Footer from "$lib/components/layout/Footer.svelte";
    import ErrorDialog from "$lib/components/feedback/ErrorDialog.svelte";

    let {children} = $props();
</script>



<div class="app">
    <main style="min-height: 95vh;">
        <Hero/>
        {@render children()}
        <ErrorDialog/>
    </main>
    <Footer/>

</div>

<!--<style>-->
<!--	.app {-->
<!--		display: flex;-->
<!--		flex-direction: column;-->
<!--		min-height: 100vh;-->
<!--	}-->

<!--	main {-->
<!--		flex: 1;-->
<!--		display: flex;-->
<!--		flex-direction: column;-->
<!--		padding: 1rem;-->
<!--		width: 100%;-->
<!--		max-width: 64rem;-->
<!--		margin: 0 auto;-->
<!--		box-sizing: border-box;-->
<!--	}-->

<!--	footer {-->
<!--		display: flex;-->
<!--		flex-direction: column;-->
<!--		justify-content: center;-->
<!--		align-items: center;-->
<!--		padding: 12px;-->
<!--	}-->

<!--	footer a {-->
<!--		font-weight: bold;-->
<!--	}-->

<!--	@media (min-width: 480px) {-->
<!--		footer {-->
<!--			padding: 12px 0;-->
<!--		}-->
<!--	}-->
<!--</style>-->
