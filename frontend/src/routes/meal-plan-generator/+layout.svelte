<script>
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
