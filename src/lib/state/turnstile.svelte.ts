export type TurnStile = 'not-verified' | 'verifying' | 'verified' | 'error';

class Turnstile {
	turnstileSetup: TurnStile;
	turnstileToken: string;

	constructor() {
		this.turnstileSetup = $state<TurnStile>('not-verified');
		this.turnstileToken = '';
	}

	changeTurnstileStatus(status: TurnStile, token?: string) {
		this.turnstileSetup = status;

		/* await axios('url') */
	}

	checkTurnstile(): boolean {
		return false;
	}

	getStatus() {
		return this.turnstileSetup;
	}
}

export const turnstile = new Turnstile();
