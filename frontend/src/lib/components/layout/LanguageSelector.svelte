<script>
    import {localeStore} from "$lib/stores/localeStore.js";

    export let floating = false;

    const languages = [
        {code: 'hu', name: 'Magyar', flag: '🇭🇺'},
        {code: 'en', name: 'English', flag: '🇬🇧'},
    ];

    $: currentLanguage = languages.find((language) => language.code === $localeStore);
    let isLanguageMenuOpen = false;

    function toggleLanguageMenu() {
        isLanguageMenuOpen = !isLanguageMenuOpen;
    }

    function closeLanguageMenu() {
        isLanguageMenuOpen = false;
    }

    function changeLanguage(lang) {
        currentLanguage = lang.code;
        isLanguageMenuOpen = false;
        localeStore.set(lang.code)
    }

    function doNothing() {
    }

</script>

<svelte:window on:click={closeLanguageMenu}/>

<div class:language-selector-container-floating={floating} class:language-selector-container={!floating}>
    <div role="button" tabindex="0" class="language-selector"
         on:click|stopPropagation={toggleLanguageMenu}
         on:keydown={doNothing()}>
            <span class="current-language">
                {currentLanguage.flag} {currentLanguage.code.toUpperCase()}
            </span>
        <span class="dropdown-icon">▼</span>

        {#if isLanguageMenuOpen}
            <div role="button" tabindex="0" on:keydown={doNothing()} class="language-dropdown" on:click|stopPropagation>
                {#each languages as language}
                    <div role="button" tabindex="0" class="language-option"
                         class:active={language.code === currentLanguage.code}
                         on:click={() => changeLanguage(language)}
                         on:keydown={doNothing()}
                    >
                        <span class="language-flag">{language.flag}</span>
                        <span class="language-name">{language.name}</span>
                    </div>
                {/each}
            </div>
        {/if}
    </div>
</div>


<style>
    .language-selector-container-floating {
        position: absolute;
        top: 0;
        right: 0;
        z-index: 10;
    }

    .language-selector-container {
        position: relative;
        display: inline-block;
    }

    .language-selector {
        display: flex;
        align-items: center;
        background-color: rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 5px 12px;
        cursor: pointer;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.2s ease;
        position: relative;
    }

    .language-selector:hover {
        background-color: rgba(255, 255, 255, 0.3);
    }

    .current-language {
        font-weight: 600;
        font-size: 0.9rem;
        margin-right: 5px;
    }

    .dropdown-icon {
        font-size: 0.7rem;
        opacity: 0.8;
        transition: transform 0.2s ease;
    }

    .language-selector:hover .dropdown-icon {
        transform: translateY(2px);
    }

    .language-dropdown {
        position: absolute;
        top: 100%;
        right: 0;
        margin-top: 5px;
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        overflow: hidden;
        width: 150px;
        z-index: 20;
        animation: fadeIn 0.2s ease;
    }

    .language-option {
        display: flex;
        align-items: center;
        padding: 10px 15px;
        cursor: pointer;
        transition: background-color 0.2s ease;
        color: #333;
        text-shadow: none;
    }

    .language-option:hover {
        background-color: #f5f5f5;
    }

    .language-option.active {
        background-color: #f0f9f7;
        font-weight: 600;
    }

    .language-flag {
        margin-right: 8px;
        font-size: 1.1rem;
    }

    .language-name {
        font-size: 0.9rem;
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes floatUp {
        from {
            transform: translateY(0);
        }
        to {
            transform: translateY(-5px);
        }
    }

    @media screen and (max-width: 768px) {
        .language-selector-container-floating {
            top: 5px;
            right: 10px;
        }

        .language-selector {
            padding: 4px 10px;
        }

        .current-language {
            font-size: 0.8rem;
        }
    }
</style>
