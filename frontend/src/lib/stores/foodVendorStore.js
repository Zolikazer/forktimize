import { writable } from 'svelte/store';

export const vendorListStore = writable([]);

export const selectedVendorStore = writable(null);
