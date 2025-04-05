import {derived, writable} from "svelte/store";
import {translations} from "$lib/localisation/translations.js";
import {CONFIG} from "$lib/config/config.js";

export const localeStore = writable(CONFIG.DEFAULT_LOCALE);

export const t = derived(localeStore, $locale => translations[$locale]);
