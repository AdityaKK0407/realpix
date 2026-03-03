export type TurnStile =
	| 'verifying'
	| 'verified'
	| 'error'
	| 'reset'
	| 'manual-verification'
	| 'save-check'
	| 'starting';

import { browser } from '$app/environment';
import axios from 'axios';
import z from 'zod';

const statusType = z.object({
	status: z.boolean()
});

class Turnstile {
	private turnstileSetup: TurnStile;
	private turnstileToken: string;
	private turnstileStatusText: string;
	private autoCheckingStatus: boolean;

	constructor() {
		this.turnstileSetup = $state<TurnStile>('starting');
		this.turnstileToken = '';
		this.turnstileStatusText = $state('Saved-Checking');
		this.autoCheckingStatus = true;
		this.init();
	}

	private async init() {
		if (browser) {
			const status = await this.checkTurnstile();
			if (!status) {
				this.turnstileSetup = 'reset';
				this.autoCheckingStatus = false;
			} else {
				this.turnstileSetup = 'verified'
			}
			this.getStatusText();
		}
	}

	changeTurnstileStatus(status: TurnStile, token?: string) {
		this.turnstileSetup = status;
		this.getStatusText();

		if(status === 'verified' && token) {
			this.turnstileToken = token;
			this.nextSteps();
		}
	}

	async checkTurnstile(): Promise<boolean> {
		const ifExists = await axios('/api/checkCookie');

		const result = statusType.safeParse(ifExists.data);
		if (!result.success) {
			return false;
		}
		return result.data.status;
	}

	getStatus() {
		return this.turnstileSetup;
	}

	shouldDisplay() {
		if(this.turnstileSetup === 'reset' && !this.autoCheckingStatus) {
			return true
		} else {
			return false
		}
	}

	private async nextSteps() {
		const response = await axios('/api/verify-turnstile', {
			method: "POST",
			data: JSON.stringify({
				turnstileToken: this.turnstileToken
			})
		})

		console.log(response.data)
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

			case 'save-check':
				text = 'Saved-Checking';
		}
		this.turnstileStatusText = text;
	}

	getStatusInfo() {
		return this.turnstileStatusText;
	}
}

export const turnstile = new Turnstile();
