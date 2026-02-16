import { writable } from 'svelte/store';

export type TurnStile = 'not-verified' | 'verifying' | 'verified';

export const turnstileSetup = writable<TurnStile>('not-verified');
