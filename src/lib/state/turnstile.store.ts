import { type Writable, writable } from 'svelte/store';

export type TurnStile = 'not-verified' | 'verifying' | 'verified';

export const turnstileSetup = writable<TurnStile>('not-verified');

class Turnstile {
	turnstileSetup: Writable<TurnStile>;
	turnstileToken: string;

	constructor() {
		this.turnstileSetup = writable<TurnStile>('not-verified')
		this.turnstileToken = '';
	}

	changeTurnstileStatus(status: TurnStile) {
		this.turnstileSetup.set(status);
	}
}

export const turnstile = new Turnstile();