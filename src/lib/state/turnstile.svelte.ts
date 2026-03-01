export type TurnStile = 'verifying' | 'verified' | 'error' | 'reset' | 'manual-verification'

class Turnstile {
	turnstileSetup: TurnStile;
	turnstileToken: string;

	constructor() {
		this.turnstileSetup = $state<TurnStile>('reset');
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
