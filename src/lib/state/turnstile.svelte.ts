export type TurnStile = 'verifying' | 'verified' | 'error' | 'reset' | 'manual-verification';

class Turnstile {
	private turnstileSetup: TurnStile;
	private turnstileToken: string;
	private turnstileStatusText: string;

	constructor() {
		this.turnstileSetup = $state<TurnStile>('reset');
		this.turnstileToken = '';
		this.turnstileStatusText = $state('In-Active');
	}

	changeTurnstileStatus(status: TurnStile, token?: string) {
		this.turnstileSetup = status;
		this.turnstileStatusText = this.getStatusText();

		/* await axios('url') */
	}

	checkTurnstile(): boolean {
		return false;
	}

	getStatus() {
		return this.turnstileSetup;
	}

	private getStatusText() {
		let text = '';
		switch (this.turnstileSetup) {
			case 'reset':
				text = 'In-Active';
				break;

			case 'verifying':
				text = 'Verifying';
				break;

			case 'verified':
				text = 'Active';
				break;

			case 'error':
				text = 'Error';
				break;

			case 'manual-verification':
				text = 'Attention';
				break;
		}
		return text;
	}

	getStatusInfo() {
		return this.turnstileStatusText;
	}
}

export const turnstile = new Turnstile();
